# 数据库更新操作
import pymysql

def showData(results):
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        # 打印结果
        print("fname=%s,lname=%s,age=%d,sex=%s,income=%d" % (fname, lname, age, sex, income))
    return

db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='abcd1234', db='test', charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL更新语句
sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('男')
query = "SELECT * FROM EMPLOYEE WHERE SEX = '%c'" %('男')
try:
    # 自行更新前先查询一下
    cursor.execute(query)
    # 获取所有记录列表
    results = cursor.fetchall()
    showData(results)
    # 执行修改语句SQL
    cursor.execute(sql)
    print(sql)
    # 执行完再查询一下
    cursor.execute(query)
    results = cursor.fetchall()
    showData(results)
    # 提交到数据库
    db.commit()
except Exception as e:
    print(repr(e))
    # 回滚
    db.rollback()
# 关闭数据库
db.close()
