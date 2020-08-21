"""
编写__enter__和__exit__仍然很繁琐，因此Python的标准库contextlib提供了更简单的写法，上面的代码可以改写如下：
"""

from contextlib import contextmanager

class Query(object):
	def __init__(self, name):
		self.name = name

	def query(self):
		print('Query info about %s...' % self.name)

@contextmanager
def create_query(name):
	print('Begin')
	q = Query(name)
	yield q
	print('End')

#@contextmanager这个decorator接受一个generator，用yield语句把with ... as var把变量输出出去，然后，with语句就可以正常地工作了：

with create_query('Bob') as q:
	q.query()

#很多时候，我们希望在某段代码执行前后自动执行特定代码，也可以用@contextmanager实现。例如：

@contextmanager
def tag(name):
	print('<%s>' % name)
	yield
	print('</%s>' % name)

with tag('h1'):
	print('Hello')
	print('Python')

"""
代码的执行顺序是：

with语句首先执行yield之前的语句，因此打印出<h1>；
yield调用会执行with语句内部的所有语句，因此打印出hello和world；
最后执行yield之后的语句，打印出</h1>。
因此，@contextmanager让我们通过编写generator来简化上下文管理。
"""