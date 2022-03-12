"""
接上，正确案例，需要通过Manager来创建Queue
"""

from multiprocessing import Process, Queue, Pool, Manager
import os, time, random

# 往队列写入操作
def write_queue(q):
    item = ['石头', '剪刀', '布']
    q.put(random.choice(item))
    
def read_queue(q):
    item = q.get()
    print(f'从队列中获取：{item}')
    
if __name__ == '__main__':
    # 定义变量名q为队列
    # 定义Manager
    manager = Manager()
    # 使用Manager主进程队列
    q = manager.Queue()
    # 定义进程池
    p = Pool()
    # 创建进程
    p.apply_async(write_queue, args=(q,))
    p.apply_async(read_queue, args=(q,))
    p.close()
    p.join()
    