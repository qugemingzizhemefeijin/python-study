"""
在Python中，读写文件这样的资源要特别注意，必须在使用完毕后正确关闭它们。正确关闭文件资源的一个方法是使用try...finally：

try:
    f = open('/path/to/file', 'r')
    f.read()
finally:
    if f:
        f.close()
写try...finally非常繁琐。Python的with语句允许我们非常方便地使用资源，而不必担心资源没有关闭，所以上面的代码可以简化为：

with open('/path/to/file', 'r') as f:
    f.read()
并不是只有open()函数返回的fp对象才能使用with语句。实际上，任何对象，只要正确实现了上下文管理，就可以用于with语句。

实现上下文管理是通过__enter__和__exit__这两个方法实现的。例如，下面的class实现了这两个方法：
"""

class Query(object):

	def __init__(self, name):
		self.name = name
	
	def __enter__(self):
		print('Begin')
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type:
			print('Error')
		else:
			print('End')

	def query(self):
		print('Query info about %s' % self.name)

with Query('Bob') as q:
	q.query()
