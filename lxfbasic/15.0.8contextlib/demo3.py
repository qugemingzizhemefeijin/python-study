"""
如果一个对象没有实现上下文，我们就不能把它用于with语句。这个时候，可以用closing()来把该对象变为上下文对象。例如，用with语句使用urlopen()：
"""

from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('https://www.baidu.com')) as page:
	for line in page:
		print(line)

"""
closing也是一个经过@contextmanager装饰的generator，这个generator编写起来其实非常简单：

@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()

它的作用就是把任意对象变为上下文对象，并支持with语句。
@contextlib还有一些其他decorator，便于我们编写更简洁的代码。
"""