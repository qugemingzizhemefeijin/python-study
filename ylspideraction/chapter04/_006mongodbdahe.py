# mongoDB使用案例
import pymongo
from bs4 import BeautifulSoup
import traceback
import requests

client = pymongo.MongoClient(host='127.0.0.1', port=27017, username="root", password="123456", authSource="test", authMechanism='SCRAM-SHA-1')
# 获取数据库
db = client['test']

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
        content = i.get_text().strip().replace(' 　　', '\n')
        db.dahe.insert_one({'content': content})
        print(content)
    except Exception as e:
        traceback.print_exc()
        
# 关闭数据库
client.close()