import redis
from bs4 import BeautifulSoup
import traceback
import requests

ip = '127.0.0.1'
port = 6379

url = 'http://xiaohua.dahe.cn/'

# 使用redis连接池
pool = redis.ConnectionPool(host=ip, port=port, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 将redis作为缓存使用，如果60s内爬取相同的数据，则不再抓取
def crawl():
    if not r.get('dahe'):   # 如果redis中无dahe则进行爬取
        res = requests.get(url)
        res.encoding='utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        r.setex('dahe', 60, res.text)
    else:
        res = r.get('dahe') # .decode(encoding='UTF-8',errors='strict')
        soup = BeautifulSoup(res, 'lxml')
        print('从缓存中读取'.center(50, '='))
    for i in soup.find_all(id="article-content"):
        try:
            content = i.get_text().strip().replace(' 　　', '\n')         # 解析并提取文字
            print(content)                                              # 打印内容
        except Exception as e:
            traceback.print_exc()
crawl()
