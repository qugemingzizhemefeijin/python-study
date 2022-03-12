"""
进程池，使用 apply_async 同步非阻塞创建和执行进程
"""

import multiprocessing
import os
import time

def run_task(name):
    print(f'任务{name} pid {os.getpid()} 正在运行，父进程 id 为 {os.getppid()}')
    time.sleep(1)
    print(f'任务 {name} 结束')
    
if __name__ == '__main__':
    print(f'当前进程为 {os.getpid()}')
    p = multiprocessing.Pool(processes = 10)
    for i in range(6):
        p.apply_async(run_task, args=(i, ))
    p.close()
    p.join()
    print('所有进程结束')
