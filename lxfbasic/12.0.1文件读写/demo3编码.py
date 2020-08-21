#字符编码
#读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数，例如，读取GBK编码的文件：

path = 'F:/python/basic/12.0.1文件读写/gbk.txt'
with open(path,'r') as f:
	print(f.read())

with open(path,'r',encoding='gb2312', errors='ignore') as f:
	print(f.read())
