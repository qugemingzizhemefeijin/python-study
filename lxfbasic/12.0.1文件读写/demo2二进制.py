#前面讲的默认都是读取文本文件，并且是UTF-8编码的文本文件。要读取二进制文件，比如图片、视频等等，用'rb'模式打开文件即可：

file='F:/python/basic/12.0.1文件读写/a.png'
f = open(file,'rb')
print(f.read())

