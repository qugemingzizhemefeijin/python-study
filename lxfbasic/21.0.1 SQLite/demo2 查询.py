#我们再试试查询记录：

import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
# 执行查询语句：
cursor.execute('select * from user where id=?', ('1',))
# 获得查询结果集
values = cursor.fetchall()
print(values)
cursor.close()
conn.close()

"""
使用Python的DB-API时，只要搞清楚Connection和Cursor对象，打开后一定记得关闭，就可以放心地使用。

使用Cursor对象执行insert，update，delete语句时，执行结果由rowcount返回影响的行数，就可以拿到执行结果。

使用Cursor对象执行select语句时，通过featchall()可以拿到结果集。结果集是一个list，每个元素都是一个tuple，对应一行记录。

如果SQL语句带有参数，那么需要把参数按照位置传递给execute()方法，有几个?占位符就必须对应几个参数，例如：

cursor.execute('select * from user where name=? and pwd=?', ('abc', 'password'))
SQLite支持常见的标准SQL语句以及几种常见的数据类型。具体文档请参阅SQLite官方网站。
"""