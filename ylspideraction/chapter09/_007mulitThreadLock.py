"""
添加锁防止并发问题
"""

import time, threading

balance = 0

def change_it_with_lock(n):
    global balance
    if lock.acquire(): # 加锁
        try:
            for i in range(1000000):
                balance = balance + n
                balance = balance - n
        finally:
            lock.release()
            
threads = [
    threading.Thread(target=change_it_with_lock, args=(5,)),
    threading.Thread(target=change_it_with_lock, args=(8,))
]
lock = threading.Lock()

[t.start() for t in threads]
[t.join() for t in threads]

print(balance)
