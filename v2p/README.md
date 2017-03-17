# 虚拟页式存储的地址转换

[piazza](https://piazza.com/class/i5j09fnsl7k5x0?cid=1012)

[题目](https://chyyuu.gitbooks.io/os_course_exercises/content/all/04-1-spoc-discussion.html)
  
## 使用说明

见` python v2p.py --h`:

```
usage: v2p.py [-h] [--memory [MEMORY]] [--disk [DISK]] [--va [VA]]
              [--PDBR [PDBR]]

example: python v2p.py --va 0x1e6f --PDBR 0xd80

optional arguments:
  -h, --help         show this help message and exit
  --memory [MEMORY]  filename of memory data
  --disk [DISK]      filename of disk data
  --va [VA]          virtual address
  --PDBR [PDBR]      page directory base register: base address of pdt
```
