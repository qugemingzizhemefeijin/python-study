import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='abcd1234', db='test', charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 如果数据表已经存在使用execute()方法删除表
cursor.execute('DROP TABLE IF EXISTS EMPLOYEE')
#创建数据库表SQL语句
sql = """CREATE TABLE EMPLOYEE(
    FIRST_NAME char(20) not null,
    LAST_NAME char(20),
    AGE int,
    SEX char(1),
    INCOME FLOAT
)"""

cursor.execute(sql)

# 关闭数据库
db.close()
