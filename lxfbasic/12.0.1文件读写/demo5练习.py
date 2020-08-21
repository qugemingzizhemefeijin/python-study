#请将本地一个文本文件读为一个str并打印出来：

fpath = r'C:\Windows\system.ini'

with open(fpath, 'r') as f:
    s = f.read()
    print(s)
