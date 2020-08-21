"""
由于MySQL服务器以独立的进程运行，并通过网络对外服务，所以，需要支持Python的MySQL驱动来连接到MySQL服务器。MySQL官方提供了mysql-connector-python驱动，但是安装的时候需要给pip命令加上参数--allow-external：

$ pip install mysql-connector-python --allow-external mysql-connector-python
如果上面的命令安装失败，可以试试另一个驱动：

$ pip install mysql-connector
我们演示如何连接到MySQL服务器的test数据库：
"""

# 导入MySQL驱动:
import mysql.connector

# 注意把password设为你的root口令:
conn = mysql.connector.connect(host='49.234.40.128',user='ad_magic_user',password='Ksslfg%123',database='ad_magic')
cursor = conn.cursor()
# 创建user表
cursor.execute('create table user(id varchar(20) primary key, name varchar(20))')
# 插入一行记录，注意MySQL的占位符是%s:
cursor.execute('insert into user(id, name) values(%s,%s)', ('1', 'Michael'))
print(cursor.rowcount)
# 创建book表
cursor.execute('create table book(id varchar(20) primary key, name varchar(20), user_id varchar(20))')
# 插入一行记录，注意MySQL的占位符是%s:
cursor.execute('insert into book(id, name, user_id) values(%s,%s,%s)', ('1', 'BookA', '1'))
# 插入一行记录，注意MySQL的占位符是%s:
cursor.execute('insert into book(id, name, user_id) values(%s,%s,%s)', ('2', 'BookB', '1'))
# 提交事务
conn.commit()
cursor.close()

# 运行查询语句
cursor = conn.cursor()
cursor.execute('select * from user where id = %s',('1',))
values = cursor.fetchall()
print(values)

# 关闭cursor和connection
cursor.close()
conn.close()

"""
由于Python的DB-API定义都是通用的，所以，操作MySQL的数据库代码和SQLite类似。

执行INSERT等操作后要调用commit()提交事务；
MySQL的SQL占位符是%s。
"""

"""
稍微正规的写法

import mysql.connector                 

# mysql1.py
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'port': 3306,
    'database': 'test',
    'charset': 'utf8'
}
try:
    cnn = mysql.connector.connect(**config)
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))
cursor = cnn.cursor()
try:
    sql_query = 'select name,age from stu ;'
    cursor.execute(sql_query)
    for name, age in cursor:
        print (name, age)
except mysql.connector.Error as e:
    print('query error!{}'.format(e))
finally:
    cursor.close()
    cnn.close()
"""