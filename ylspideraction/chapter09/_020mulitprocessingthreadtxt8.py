"""
多进程多线程抓取案例
"""


from multiprocessing import Process, Queue, Pool, Manager, Lock
import os, time, random, requests, traceback, json, threading
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017, username="root", password="123456", authSource="test", authMechanism='SCRAM-SHA-1')
# 获取数据库，初始化数据库
db = client['test']

site = 'http://www.txt8.net'
# 伪装请求头
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

# 列表函数
def list_page(q, num):
    print('start mission')
    
    try:
        for index in range(1, num) :
            url = '%s/sort/dushi/%s.html' %(site, index)
            print('抓取 url = %s' % url)
            res = requests.get(url, headers = headers).text
            soup = BeautifulSoup(res, 'lxml')
            page_data = []
            for i in soup.find('ul', class_='librarylist').find_all('li'):
                try:
                    left = i.find('div', class_='pt-ll-l')
                    right = i.find('div', class_='pt-ll-r')
                    
                    title = left.find('a').get('title').strip()
                    url = site + left.find('a').get('href').strip()
                    pic = site + left.find('img')['src'].strip()
                    
                    author = right.find_all('a')[1].get_text().strip()
                    content = right.find('p', class_='intro').get_text().strip()
                    
                    item = {'title': title, 'url': url, 'pic': pic, 'author': author, 'content': content}
                    #print(json.dumps(item, ensure_ascii=False))
                    
                    page_data.append(item)
                except Exception as e:
                    traceback.print_exc()
            print('抓取数量：%s' % len(page_data))
            q.put(page_data)
    except:
        traceback.print_exc()
    
    # 抓取完成，让子进程退出循环
    time.sleep(10)
    q.put('exit')
        
# 进程中的子线程尽心抓取保存工作
def download_thread(item):
    try:
        db.txt8.insert_one(item)
    except:
        traceback.print_exc()
            
# 保存函数
def download(q):
    print('子进程开启==========')
    # 开启无线循环
    while True:
        # 从队列获取名字和url
        page_data = q.get()
        if page_data == 'exit':
            break
        print(f'子进程 {os.getpid()} 开启线程池获取数据，本次待抓取数量：{len(page_data)}')
        
        # 建立拥有2个线程的线程池
        pool = ThreadPoolExecutor(2)
        # 通过map映射列表调用hello函数
        pool.map(download_thread, page_data)
        # 等待任务完成，关闭线程池
        pool.shutdown(wait = True)
        
if __name__ == '__main__':
    print('初始化数据库')
    # 清空数据
    db.txt8.delete_many({})
    print('数据库初始化完成')
    print('开始抓取数据')
    manager = Manager()
    # 使用Manager主进程队列
    q = manager.Queue()
    # 定义进程池
    p = Pool()
    # 创建进程
    p.apply_async(list_page, args=(q, 11, ))
    p.apply_async(download, args=(q, ))
    p.close()
    p.join()
    print('完成抓取工作')
    # 关闭数据库
    client.close()
