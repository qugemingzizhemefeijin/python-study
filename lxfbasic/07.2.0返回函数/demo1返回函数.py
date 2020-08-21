"""
函数作为返回值

高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。
我们来实现一个可变参数的求和。通常情况下，求和的函数是这样定义的：
"""

def calc_sum(*args):
	ax = 0
	for n in args:
		ax = ax + n
	return ax

#但是，如果不需要立刻求和，而是在后面的代码中，根据需要再计算怎么办？可以不返回求和的结果，而是返回求和的函数：

def lazy_sum(*args):
	def sum():
		ax = 0
		for n in args:
			ax = ax + n
		return ax
	return sum

#当我们调用lazy_sum()时，返回的并不是求和结果，而是求和函数：

f = lazy_sum(1, 3, 5, 7, 9)
print(f)
print(type(f))

#调用函数f时，才真正计算求和的结果：
print(f())

"""
在这个例子中，我们在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，当lazy_sum返回函数sum时，
相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力。

请再注意一点，当我们调用lazy_sum()时，每次调用都会返回一个新的函数，即使传入相同的参数：
"""

f1 = lazy_sum(1, 3, 5, 7, 9)
f2 = lazy_sum(1, 3, 5, 7, 9)
print(f1 == f2)

#f1()和f2()的调用结果互不影响。

