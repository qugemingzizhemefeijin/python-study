# metaclass是类的模板，所以必须从`type`类型派生：
class ListMetaclass(type):

    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        print("===============11============")
        return type.__new__(cls, name, bases, attrs)

class MyList(list):

	def __init__(self, **kw):
		print('==========1111=============')
		super().__init__(**kw)

	def __getattr__(self, key):
		return self[key]

class MeList(MyList, metaclass=ListMetaclass):

	def __init__(self, **kw):
		super().__init__(**kw)

L = MeList()
L.add(1)
print(L)