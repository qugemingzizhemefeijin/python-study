# master.py

import requests
from bs4 import BeautifulSoup
from _002slave import crawler

# python _002master.py

# 这个相当于将任务全部提交给slave来让slave异步进行下载

url = 'http://docs.celeryproject.org/en/latest/'
res = requests.get(url)
# 解析网页
soup = BeautifulSoup(res.text, 'html.parser')
for i in soup.find_all('a'):
    link = i.get('href')
    if 'www' not in link and not '#' in link:
        link = url + link
        print(link)
        result = crawler.delay(link)    # 将url传入任务抓取数据
