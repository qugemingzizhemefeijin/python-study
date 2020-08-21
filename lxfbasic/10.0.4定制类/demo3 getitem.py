"""
Fib实例虽然能作用于for循环，看起来和list有点像，但是，把它当成list来使用还是不行，比如，取第5个元素：

要表现得像list那样按照下标取出元素，需要实现__getitem__()方法
"""

class Fib(object):
	
	def __iter__(self):
		return self

	def __next__(self):
		self.a,self.b = self.b, self.a+self.b
		if self.a > 10000:
			raise StopIteration()
		return self.a

	def __getitem__(self, n):
		a, b = 1,1
		for x in range(n):
			a, b = b, a+b
		return a

f = Fib()

print(f[0])
print(f[1])
print(f[2])
print(f[3])
print(f[100])