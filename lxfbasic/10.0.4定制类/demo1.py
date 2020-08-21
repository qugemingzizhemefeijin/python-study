"""
怎么才能打印类实例好看呢？只需要定义好__str__()方法，返回一个好看的字符串就可以了（跟java的toString()相似）

但是在终端执行下面代码的话，细心的朋友会发现直接敲变量不用print，打印出来的实例还是不好看

这是因为直接显示变量调用的不是__str__()，而是__repr__()，两者的区别是__str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，也就是说，__repr__()是为调试服务的。

解决办法是再定义一个__repr__()。但是通常__str__()和__repr__()代码都是一样的，所以，有个偷懒的写法
"""

class Student(object):
	def __init__(self,name):
		self.name=name
	
	def __str__(self):
		return 'Student object (name: %s)' % self.name

	__repr__ = __str__

michael = Student('Michael')
print(michael)
