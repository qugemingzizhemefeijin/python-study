"""
多线程并发的问题，结果应该打印的是0,0，但是因为并发打印的有时候未符合预期
"""

import threading, time

balance = 0

def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n
    
# 运行一百万次打印余额
def run_thread(n):
    for i in range(1000000):
        change_it(n)
    global balance
    print(balance)
    
t1 = threading.Thread(target=run_thread, args=(5,)) # 初始化5
t2 = threading.Thread(target=run_thread, args=(8,)) # 初始化8

t1.start()
t2.start()
t1.join()
t2.join()

print("=============")
