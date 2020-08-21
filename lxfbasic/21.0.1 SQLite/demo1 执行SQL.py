#SQLite是一种嵌入式数据库，它的数据库就是一个文件。由于SQLite本身是C写的，而且体积很小，所以，经常被集成到各种应用程序中，甚至在iOS和Android的App中都可以集成。
#Python就内置了SQLite3，所以，在Python中使用SQLite，不需要安装任何东西，直接使用。

# 导入SQLite驱动:
import sqlite3

# 连接到SQLite数据库
# 数据库文件是test.db
# 如果文件不存在，会自动在当前目录创建:
conn = sqlite3.connect('test.db')
# 创建一个Cursor:
cursor = conn.cursor()
# 执行一条SQL语句，创建user表
cursor.execute('create table user(id varchar(20) primary key, name varchar(20))')
# 继续执行一条SQL语句，插入一条记录：
cursor.execute('insert into user(id,name) values("1", "Michael")')
# 通过rowcount获取插入的行数
print(cursor.rowcount)
# 关闭cursor
cursor.close()
# 提交事务
conn.commit()
# 关闭Connection:
conn.close()
