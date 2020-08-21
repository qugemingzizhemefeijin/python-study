#如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本：

def log(text):
	def decorator(func):
		def wrapper(*args, **kw):
			print('%s %s():' %(text, func.__name__))
			return func(*args, **kw)
		return wrapper
	return decorator

@log('execute')
def now():
	print('2020-02-02')

now()

#和两层嵌套的decorator相比，3层嵌套的效果是这样的：
#now = log('execute')(now)

#我们来剖析上面的语句，首先执行log('execute')，返回的是decorator函数，再调用返回的函数，参数是now函数，返回值最终是wrapper函数。

