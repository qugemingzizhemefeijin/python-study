"""
但是list有个神奇的切片方法
对于Fib却报错。原因是__getitem__()传入的参数可能是一个int，也可能是一个切片对象slice，所以要做判断

也没有对负数作处理，所以，要正确实现一个__getitem__()还是有很多工作要做的。
此外，如果把对象看成dict，__getitem__()的参数也可能是一个可以作key的object，例如str。
与之对应的是__setitem__()方法，把对象视作list或dict来对集合赋值。最后，还有一个__delitem__()方法，用于删除某个元素。
总之，通过上面的方法，我们自己定义的类表现得和Python自带的list、tuple、dict没什么区别，这完全归功于动态语言的“鸭子类型”，不需要强制继承某个接口。
"""

class Fib(object):
	def __getitem__(self,n):
		if isinstance(n, int):	#n是索引
			a, b = 1, 1
			for x in range(n):
				a, b = b, a+b
			return a
		elif isinstance(n, slice):	#n是切片
			start = n.start
			stop = n.stop
			if start is None:
				start = 0
			a, b = 1,1
			L = []
			for x in range(stop):
				if x >= start:
					L.append(a)
				a , b = b, a+b
			return L

f = Fib()
print(f[:5])
print(f[1:3])
#但是没有对step参数作处理
print(f[1:3:2])
