"""
concurrent.futures 线程池模块
"""

import time
from concurrent.futures import ThreadPoolExecutor

def hello(n):
    print('此线程等待%d秒' % n)
    time.sleep(n)
    
if __name__ == '__main__':
    start = time.time()
    # 建立拥有5个线程的线程池
    pool = ThreadPoolExecutor(5)
    # 任务列表
    delay_list = [1, 2, 3, 4, 5]
    # 通过map映射列表调用hello函数
    pool.map(hello, delay_list)
    # 等待任务完成，关闭线程池
    pool.shutdown(wait = True)
    # 打印时间
    print(time.time() - start)
