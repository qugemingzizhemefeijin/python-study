"""
在面向对象（OOP）的设计模式中，decorator被称为装饰模式。OOP的装饰模式需要通过继承和组合来实现，而Python除了能支持OOP的decorator外，直接从语法层次支持decorator。
Python的decorator可以用函数实现，也可以用类实现。

decorator可以增强函数的功能，定义起来虽然有点复杂，但使用起来非常灵活和方便。

请编写一个decorator，能在函数调用的前后打印出'begin call'和'end call'的日志。

再思考一下能否写出一个@log的decorator，使它既支持：

@log
def f():
    pass


又支持：

@log('execute')
def f():
    pass
"""

import functools

def log(func):
	if isinstance(func, str):
		def decorator(fn):
			#@functools.wraps(fn)
			def wrapper(*args, **kw):
				print('begin call %s' % fn.__name__)
				a = fn(*args, **kw)
				print('end call %s' % fn.__name__)
				return a
			return wrapper
		return decorator
	else:
		#@functools.wraps(func)
		def wrapper(*args, **kw):
			print('begin call %s' % func.__name__)
			a=func(*args, **kw)
			print('end call %s' % func.__name__)
			return a
		return wrapper

@log
def f():
	print('======')

@log('abc')
def x():
	print('+++++++++')

f()
x()