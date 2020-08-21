class Field(object):

	def __init__(self, name, column_type):
		self.name = name
		self.column_type = column_type

	def __str__(self):
		return "<%s,%s>" % (self.__class__.__name__, self.name)


class StringField(Field):

	def __init__(self, name):
		super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):

	def __init__(self, name):
		super(IntegerField, self).__init__(name, 'bigint')

class DoubleField(Field):

	def __init__(self, name):
		super().__init__(name, 'double')


class ModelMetaClass(type):
	
	"""
	cls 当前准备创建的类的对象；
	name 类的名字；
	bases 类继承的父类集合；
	attrs 类的方法集合。
	"""
	def __new__(cls, name, bases, attrs):
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)
		print('Found model: %s' % name)
		mappings = dict()
		for k,v in attrs.items():
			if isinstance(v, Field):
				print('Found Mapping: %s ==> %s ==> %s' % (k, v, v.column_type))
				mappings[k] = v
		for k in mappings.keys():
			attrs.pop(k)
		
		attrs['__mappings__'] = mappings	# 保存属性和列的映射关系
		attrs['__table__'] = name	# 假设表名和类名一致
		return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaClass):
	
	def __init__(self, **kw):
		super().__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

	def save(self):
		fields = []
		params = []
		args = []

		for k,v in self.__mappings__.items():
			fields.append(v.name)
			params.append('?')
			args.append(getattr(self, k, None))

		sql = 'insert into %s (%s) values(%s)' % (self.__table__, ','.join(fields), ','.join(params))
		print('SQL: %s' % sql)
		print('ARGS: %s' % str(args))

class User(Model):
	# 定义类的属性到列的映射
	id = IntegerField('id')
	name = StringField('username')
	email = StringField('email')
	password = StringField('password')
	money = DoubleField('money')

#创建user实例
u = User(id=1234, name='Michael', email='chengang@tom.com', password='abcdef', money=1.2)
#保存到数据库
u.save()