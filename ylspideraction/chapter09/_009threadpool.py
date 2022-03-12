"""
threadpool 线程池，现在 threadpool 已经不是主流的线程池模块了，python3新增了 concurrent.futures
"""

import threadpool, time

def hello(delay):
    print('此线程等待%d秒' % delay)
    time.sleep(delay)
    
if __name__ == '__main__':
    # 获取开始时间
    start = time.time()
    # 创建线程池，指定5个
    pool = threadpool.ThreadPool(5)
    # 创建任务列表
    delay_list = [1, 2, 3, 4, 5]
    # 创建任务
    task = threadpool.makeRequests(hello, delay_list)
    # 通过遍历将任务传入线程池中执行
    for i in task:
        pool.putRequest(i)
    # [pool.putRequest(i) for i in task]
    # 等待线程执行结束
    pool.wait()
    # 打印代码运行花费的时间
    print(time.time() - start)
