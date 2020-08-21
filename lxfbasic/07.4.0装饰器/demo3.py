#以上两种decorator的定义都没有问题，但还差最后一步。因为我们讲了函数也是对象，它有__name__等属性，但你去看经过decorator装饰之后的函数，它们的__name__已经从原来的'now'变成了'wrapper'：

#print(now.__name__)
#'wrapper'

#因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。
#不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的，所以，一个完整的decorator的写法如下：

import functools

def log(func):
	@functools.wraps(func)
	def wrapper(*args, **kw):
		print('call %s()'%func.__name__)
		return func(*args, **kw)
	return wrapper

#或者针对带参数的decorator：

def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			print('%s %s():'%(text, func.__name__))
			return func(*args, **kw)
		return wrapper
	return decorator


