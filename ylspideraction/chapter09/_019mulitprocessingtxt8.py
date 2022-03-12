"""
多进程抓取txt8小说列表页介绍。

通过爬取列表页，从列表页获取所有的小说名称，作者和简介并写入到队列。然后download函数从队列中获取信息并写入到本地文件中。

http://www.txt8.net/sort/dushi/1.html
"""

from multiprocessing import Process, Queue, Pool, Manager, Lock
import os, time, random, requests, traceback, json
from bs4 import BeautifulSoup

site = 'http://www.txt8.net'
# 伪装请求头
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

# 列表函数
def list_page(url, q, num):
    print('start mission')
    # 清空文件
    with open('E:/tmp/txt8.txt', 'w') as f:
        f.write('')
    res = requests.get(url, headers = headers).text
    soup = BeautifulSoup(res, 'lxml')
    
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
            
            q.put(item)
        except Exception as e:
            traceback.print_exc()
    # 抓取完成，让子进程退出循环
    time.sleep(6)
    for i in range(num):
        q.put('exit')
            
# 保存函数
def download(q, lock):
    # 开启无线循环
    while True:
        # 从队列获取名字和url
        item = q.get()
        print(f'子进程 {os.getpid()} 获取数据 {item}')
        if item == 'exit':
            break
        lock.acquire()  # 锁住
        try:
            with open('E:/tmp/txt8.txt', 'a+') as f:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
            print('文件保存成功')
        except:
            traceback.print_exc()
        finally:
            lock.release()
        
if __name__ == '__main__':
    url = site + '/sort/dushi/1.html'
    print('待抓取：' + url)
    manager = Manager()
    # 使用Manager主进程队列
    q = manager.Queue()
    # 使用Lock
    lock = manager.Lock()
    # 定义进程池
    p = Pool()
    # 创建进程
    p.apply_async(list_page, args=(url, q, 2, ))
    p.apply_async(download, args=(q, lock, ))
    p.apply_async(download, args=(q, lock, ))
    p.close()
    p.join()
    print('完成')

