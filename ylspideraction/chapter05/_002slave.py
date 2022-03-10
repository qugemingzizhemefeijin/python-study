# slave.py

from celery import Celery
import requests
import time
from bs4 import BeautifulSoup

# celery -A _002slave worker -l info -P eventlet

app = Celery('tasks', broker='redis://127.0.0.1/0', backend='redis://127.0.0.1/1')

# 将爬虫函数注册为一个任务
@app.task
def crawler(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find('h1').get_text().strip()
    f = open('E:/tmp/xx/%s.txt'%title, 'w+')
    f.write(url)
    f.close()
