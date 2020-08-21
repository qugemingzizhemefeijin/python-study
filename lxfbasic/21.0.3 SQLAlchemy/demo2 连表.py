"""
由于关系数据库的多个表还可以用外键实现一对多、多对多等关联，相应地，ORM框架也可以提供两个对象之间的一对多、多对多等功能。

"""

# 导入
from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from urllib import parse

# 创建对象的基类
Base = declarative_base()

# 定义User对象
class User(Base):
	# 表的名字:
	__tablename__ = 'user'

	# 表的结构
	id = Column(String(20), primary_key=True)
	name = Column(String(20))
	# 一对多:
	books = relationship('Book')

# 定义Book对象
class Book(Base):
	# 表的名字：
	__tablename__ = 'book'

	# 表的结构
	id = Column(String(20) , primary_key=True)
	name = Column(String(20))
	# 多的一方的book表中设置了一个外键字段user_id,这个字段保存了属于哪个用户,通过这个外键指向user对象
	# 千万要记住 ForeignKey(数据库名.字段名) book表的外键对应的是用户表的id主键,要一定注意大小写
	user_id = Column(String(20), ForeignKey('user.id'))


# 在连接前将特殊的密码转码再链接即可
passowrd = parse.quote_plus('Ksslfg%123')

# 初始化数据库连接
engine = create_engine('mysql+mysqlconnector://ad_magic_user:%s@49.234.40.128:3306/ad_magic' % passowrd, encoding='utf-8', echo=False)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

session = DBSession()
user = session.query(User).filter(User.id=='1').one()
print(user)
print(user.name)
print(user.books)

for book in user.books:
	print('book id = %s, name=%s' %(book.id, book.name))

session.close()
