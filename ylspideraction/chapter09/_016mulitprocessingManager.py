"""
如果使用了Pool创建了子进程后，就没法用 multiprocessing.Queue直接通信了。
需要通过Manager来进行管理并中转。
下面是错误案例，结果为什么都没打印
"""

from multiprocessing import Process, Queue, Pool, Manager
import os, time, random

# 往队列写入操作
def write_queue(q):
    item = ['石头', '剪刀', '步']
    q.put(random.choice(item))
    
def read_queue(q):
    item = q.get()
    print(f'从队列中获取：{item}')
    
if __name__ == '__main__':
    # 定义变量名q为队列
    q = Queue()
    # 定义进程池
    p = Pool()
    # 创建进程
    p.apply_async(write_queue, args=(q,))
    p.apply_async(read_queue, args=(q,))
    p.close()
    p.join()
    
