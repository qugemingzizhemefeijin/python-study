"""
# 引入队列
import queue
# 设置队列容量
workQueue = queue.Queue(10)
# 通过循环往队列写入数据
for i in change(10):
    workQueue.put(i)
# 查看当前队列的数量
workQueue.qsize()
# 查看当前队列是否为空
workQueue.empty()
# 用非堵塞的方式从队列获取元素，获得数字元素0，如果队列为空会抛出异常
workQueue.get_nowait()
# 用非堵塞的方式从队列获取元素，获得数字元素1，如果队列为空会抛出异常
workQueue.get_nowait()
# 查看队列当前的数量
workQueue.empty()
"""

import time, threading, queue

balance = 0
workQueue = queue.Queue(10) # 定义队列
workQueue.put(balance)

def change_it(n):
    global balance
    balance = workQueue.get() # 从队列中提取余额
    balance = balance + n
    balance = balance - n
    workQueue.put(balance)

def run_thread(n):
    for i in range(1000000):
        change_it(n)
    global balance
    print(balance)
    
t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))

# 开启线程
t1.start()
t2.start()
t1.join()
t1.join()
