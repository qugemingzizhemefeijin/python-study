"""
python多进程
"""

from multiprocessing import Process
import os

# info 函数，获取进程信息
def info(title):
    print(title)
    print('模块名：', __name__)
    print('父进程：', os.getppid())
    print('进程ID：', os.getpid())

# f函数，在函数内调用info函数
def f(name):
    print('hello', name, '这里是子进程')
    info('函数 f')
    
if __name__ == '__main__':
    # 使用主进程调用info
    info('主进程')
    # 开启子进程调用f函数，并在f函数内调用info函数，获取子进程信息
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
