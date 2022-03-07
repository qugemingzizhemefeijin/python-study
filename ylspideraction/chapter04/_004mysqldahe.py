# -*- coding: utf-8 -*-

# 将从大河笑话上抓取的笑话存储到数据库中
import pymysql
from bs4 import BeautifulSoup
import traceback
import requests

# 连接数据库
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='abcd1234', db='test', charset='utf8mb4')
# 获取游标
cursor = db.cursor()

# 如果已存在表，则删除
cursor.execute('DROP TABLE IF EXISTS dahe')
# 建表语句
sql = """
create table dahe(
id bigint(20) not null primary key auto_increment comment 'ID',
context text)
"""
cursor.execute(sql)

# 抓取大河笑话
url = 'http://xiaohua.dahe.cn/'
res = requests.get(url)
res.encoding='utf-8'
# print(res.apparent_encoding)
# 使用beautifulsoup进行解析
soup = BeautifulSoup(res.text, 'lxml')
data = []
for i in soup.find_all(id="article-content"):
    try:
        #print(i.get_text().strip())
        content = i.get_text().strip()
        sql = """
            insert into dahe(context) values('%s');
            """ % content
        # print(sql)
        cursor.execute(sql)
        print(content)
    except Exception as e:
        traceback.print_exc()
# 提交数据
db.commit()
# 关闭数据库连接
cursor.close()
db.close()
