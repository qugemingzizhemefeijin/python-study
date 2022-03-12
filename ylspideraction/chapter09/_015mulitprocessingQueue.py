"""
进程间的队列，通过 multiprocessing.Queue来实现的。

两个进程，一个写，一个读。
"""

from multiprocessing import Process, Queue
import os, time, random
import queue

# 往队列中写入操作
def write_queue(q):
    item = ['石头', '剪刀', '布']
    a = random.choice(item)
    q.put(a)
    print(f'写入队列中 {a}, pid = {os.getpid()}')
    
# 从队列取出操作
def read_queue(q):
    item = q.get()
    print(f'从队列中获取{item}，pid = {os.getpid()}')
    
if __name__ == '__main__':
    # 定义变量名q为队列
    q = Queue()
    # 创建进程
    t1 = Process(target=write_queue, args=(q,))
    t2 = Process(target=read_queue, args=(q,))
    # 开启子进程t2并等待进程结束
    t1.start()
    t1.join()
    # 开启子进程t2并等待进程结束
    t2.start()
    t2.join()
