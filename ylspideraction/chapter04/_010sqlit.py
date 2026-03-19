"""
sqlit3是python2.5之后就自带的，不需要额外安装
"""

#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('E:/test.db')

print("数据库打开成功")

c = conn.cursor()

# 获取一个表的数据
cursor = c.execute("SELECT iclassid, ccoursecname from courseclass")
classMap = dict(map(lambda x: (x[0], x[1]), list(cursor)))
    
# 迭代表
cursor = c.execute("SELECT isubclassid, csubclassname, iclassid, iindex, dchangedate from coursesubclass")
for row in cursor:
   print("ID = ", row[0], ', 名称 = ', row[1], ', 分类 = ', classMap[row[2]])
   
print('华丽的分割符'.center(50, '*'))

c.execute('DROP TABLE IF EXISTS COMPANY')
c.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
print ("数据表创建成功")

print('华丽的分割符'.center(50, '*'))

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
print ("数据插入成功")

print('华丽的分割符'.center(50, '*'))

cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print("ID = ", row[0], ",NAME = ", row[1], ",ADDRESS = ", row[2], ",SALARY = ", row[3])
   
print('华丽的分割符'.center(50, '*'))

c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
print("Total number of rows updated :", conn.total_changes)

cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print("ID = ", row[0], ",NAME = ", row[1], ",ADDRESS = ", row[2], ",SALARY = ", row[3])
   
print('华丽的分割符'.center(50, '*'))

c.execute("DELETE from COMPANY where ID=2;")
print("Total number of rows deleted :", conn.total_changes)

cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print("ID = ", row[0], ",NAME = ", row[1], ",ADDRESS = ", row[2], ",SALARY = ", row[3])

# 如果您未调用该方法，那么自您上一次调用 commit() 以来所做的任何动作对其他数据库连接来说是不可见的。
conn.commit()
# 该方法关闭数据库连接。请注意，这不会自动调用 commit()。如果您之前未调用 commit() 方法，就直接关闭数据库连接，您所做的所有更改将全部丢失！
conn.close()

