#写文件
#写文件和读文件是一样的，唯一区别是调用open()函数时，传入标识符'w'或者'wb'表示写文本文件或写二进制文件：

path='F:/python/basic/12.0.1文件读写/ww.txt'

#你可以反复调用write()来写入文件，但是务必要调用f.close()来关闭文件。当我们写文件时，操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入。
#只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘。忘记调用close()的后果是数据可能只写了一部分到磁盘，剩下的丢失了。所以，还是用with语句来得保险：

with open(path,'w') as f:
	f.write('Hello Write Python!')


with open(path,'r') as f:
	print(f.read())

"""
要写入特定编码的文本文件，请给open()函数传入encoding参数，将字符串自动转换成指定编码。
细心的童鞋会发现，以'w'模式写入文件时，如果文件已存在，会直接覆盖（相当于删掉后新写入一个文件）。如果我们希望追加到文件末尾怎么办？可以传入'a'以追加（append）模式写入。
所有模式的定义及含义可以参考Python的官方文档。

https://docs.python.org/3/library/functions.html#open
"""

