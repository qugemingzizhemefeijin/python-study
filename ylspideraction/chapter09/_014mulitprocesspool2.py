"""
进程池，使用map同步非阻塞创建和执行进程

map传递参数只能传递一个，如果需要传递多个，则需要对参数进行封装。
map是阻塞的，apply_async是非阻塞的
map可以返回结果，而apply_async不能返回结果
"""

from multiprocessing import Pool
import os
import time

def run_task(name):
    print(f'任务{name} pid {os.getpid()} 正在运行，父进程 id 为 {os.getppid()}')
    time.sleep(1)
    print(f'任务 {name} 结束')
    
if __name__ == '__main__':
    print(f'当前进程为 {os.getpid()}')
    # 指定10个进程
    pool = Pool(10)
    # 使用列表推导式创建任务列表
    number = [i for i in range(6)]
    # 传入任务名列表，通过map进行映射，创建子进程调用run函数
    pool.map(run_task, number)
    pool.close()
    pool.join()
    print('所有进程结束')
