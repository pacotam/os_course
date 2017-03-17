import argparse


def parse_args():
    '''
    Parses the node2vec arguments.
    '''
    parser = argparse.ArgumentParser(description="example: python v2p.py --va 0x1e6f --PDBR 0xd80")

    parser.add_argument('--memory', nargs='?', default='mem.txt',
                        help='filename of memory data')
    parser.add_argument('--disk', nargs='?', default='disk.txt',
                        help='filename of disk data')
    parser.add_argument('--va', nargs='?',
                        help='virtual address')
    parser.add_argument('--PDBR', nargs='?', default='0x220',
                        help='page directory base register: base address of pdt')

    return parser.parse_args()


def read_memory(memory):
    # memory or disk
    # mem[pfn] = 32 bytes
    # mem[pfn][off] -> (pfn << 5) | off :phy addr
    mem = {}
    f = open(memory, 'r')
    for line in f:
        l = line.split(':')
        pfn = int(l[0].split()[1], 16)
        pf = map((lambda x: int(x, 16)), l[1].split())
        mem[pfn] = pf
    f.close()
    return mem


def v2p(mem, disk, pdbr, va):
    pdbr_pfn = pdbr >> 5
    offset = va & 0x1f
    pte_index = (va >> 5) & 0x1f
    pde_index = (va >> 10) & 0x1f
    print 'Virtual Address ' + hex(va) + ':'
    pde_content = look_up(mem, pdbr_pfn, pde_index)
    print '\t--> pde index: ' + hex(pde_index) \
          + '  pde contents:(valid ' + str(pde_content[0]) \
          + ', pfn ' + hex(pde_content[1]) + ')'
    if pde_content[0] == 1:
        # valid, in memory
        pte_content = look_up(mem, pde_content[1], pte_index)
        print '\t\t--> pte index: ' + hex(pte_index) \
              + '  pte contents:(valid ' + str(pte_content[0]) \
              + ', pfn ' + hex(pte_content[1]) + ')'
        if pte_content[0] == 1:
            print '\t\tin memory:'
            pa = (pte_content[1] << 5) | offset
            value = mem[pte_content[1]][offset]
            print '\t\t\t--> Translates to Physical Address ' + hex(pa) + ' --> Value: ' + hex(value)
        elif pte_content[1] != 0x7f:
            print '\t\tin disk:'
            pa = (pte_content[1] << 5) | offset
            value = disk[pte_content[1]][offset]
            print '\t\t\t--> Translates to Disk Sector Address ' + hex(pa) + ' --> Value: ' + hex(value)
        else:
            print '\t\tnot exist:'
            print '\t\t\t--> Fault (page table entry not valid)'
    else:
        # not valid
        print '\t\t--> Fault (page directory entry not valid)'


def look_up(mem, pfn, index):
    content = mem[pfn][index]
    # valid | pfn6~0
    return content >> 7, content & 0x7f


if __name__ == '__main__':
    args = parse_args()
    mem = read_memory(args.memory)
    disk = read_memory(args.disk)
    v2p(mem, disk, int(args.PDBR, 16), int(args.va, 16))
