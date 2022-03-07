# mysql 查询
import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='abcd1234', db='test', charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 查询语句
sql = "select * from EMPLOYEE \
    where INCOME > '%d'" % (1000)
print(sql)
    
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        # 打印结果
        print("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % (fname, lname, age, sex, income))
except Exception as e:
    print(e.args)
    print(str(e))
    print(repr(e))
    print('Error: unable to fecth data')
# 关闭数据库连接
db.close()