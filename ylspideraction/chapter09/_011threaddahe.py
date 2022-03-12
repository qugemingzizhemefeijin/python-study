"""
实战案例，大河笑话抓取
"""

import requests
import threading
import queue
from bs4 import BeautifulSoup
import time
import traceback
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

# 任务队列
workQueue = queue.Queue(400)
# 存放列表页url
link_list = []

def start(url):
    res = requests.get(url, headers = headers)
    res.encoding = 'utf-8'
    # 解析源码
    soup = BeautifulSoup(res.text, 'lxml')
    for i in range(1,3):
        link = 'http://xiaohua.dahe.cn/index-%d.html' % i
        # 将重构的url存入到列表中
        link_list.append(link)
        
def listPage(url):
    # 发送请求
    res = requests.get(url, headers = headers)
    res.encoding = 'utf-8'
    # 解析源码
    soup = BeautifulSoup(res.text, 'lxml')
    # 循环遍历列表页中每一个详情页的标题
    for i in soup.find('ul', id='content').find_all('li'):
        try:
            url = i.find('h4').find('a').get('href')
            title = i.find('h4').find('a').get_text().strip()
            content = i.find('div', id='article-content').get_text().strip()
            
            item = {'url': url, 'title': title, 'content': content}
            
            # 将数据存入队列中
            workQueue.put(item)
        except Exception as e:
            traceback.print_exc()

def save_file():
    # 使用while开启无限循环，保持挂起状态
    while True:
        # 从队列中获取任务，只使用get方法，如果使用get_nowait方法，队列为空则会抛出异常
        item = workQueue.get()
        if(item == 'exit'):
            break
        # 以追加模式，打开文件
        f = open('E:/tmp/dahe.txt', 'a+')
        # 写入内容
        f.writelines(json.dumps(item, ensure_ascii=False) + '\n')
        f.close()
        
def exit():
    time.sleep(6)
    workQueue.put('exit')
        
if __name__ == '__main__':
    url = 'http://xiaohua.dahe.cn/'
    # 启动start
    start(url)
    # 多线程列表
    thread_list = []
    # 遍历创建线程
    for i in link_list:
        thread_item = threading.Thread(target=listPage, args=[i])
        thread_list.append(thread_item)
    # 单独将save_file线程加入到线程列表
    thread_list.append(threading.Thread(target=save_file))
    # 在第10秒之后，存储一个退出的指令
    thread_list.append(threading.Thread(target=exit))
    # 遍历开启线程
    [t.start() for t in thread_list]
    # 遍历等待
    [t.join() for t in thread_list]
    print('===' * 5)
    
        
    
                
