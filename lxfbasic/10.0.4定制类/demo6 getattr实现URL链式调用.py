"""
现在很多网站都搞REST API，比如新浪微博、豆瓣啥的，调用API的URL类似：

http://api.server/user/friends
http://api.server/user/timeline/list
如果要写SDK，给每个URL对应的API都写一个方法，那得累死，而且，API一旦改动，SDK也要改。

利用完全动态的__getattr__，我们可以写出一个链式调用：
"""

class Chain(object):
	def __init__(self, path=''):
		self._path = path

	def __getattr__(self, path):
		print(path)
		return Chain('%s/%s' % (self._path, path))
	
	def __str__(self):
		return self._path

	__repr__ = __str__

print(Chain().status.user.timeline.list)
