#读文件
#要以读文件的模式打开一个文件对象，使用Python内置的open()函数，传入文件名和标示符：

path = 'F:/python/basic/12.0.1文件读写/test.txt'

f = open(path,'r')
s = f.read()
f.close()

print(s)

#由于文件读写时都有可能产生IOError，一旦出错，后面的f.close()就不会调用。所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现：
try:
	f = open(path, 'r')
	print(f.read())
finally:
	if f:
		f.close()

#但是每次都这么写实在太繁琐，所以，Python引入了with语句来自动帮我们调用close()方法：
with open(path, 'r') as f:
	print(f.read())

#这和前面的try ... finally是一样的，但是代码更佳简洁，并且不必调用f.close()方法。
#调用read()会一次性读取文件的全部内容，如果文件有10G，内存就爆了，所以，要保险起见，可以反复调用read(size)方法，每次最多读取size个字节的内容。
#另外，调用readline()可以每次读取一行内容，调用readlines()一次读取所有内容并按行返回list。因此，要根据需要决定怎么调用。
#如果文件很小，read()一次性读取最方便；如果不能确定文件大小，反复调用read(size)比较保险；如果是配置文件，调用readlines()最方便：

with open(path, 'r') as f:
	for line in f.readlines():
		print(line.strip())