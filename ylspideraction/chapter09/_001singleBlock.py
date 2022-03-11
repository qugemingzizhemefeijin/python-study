"""
单线程阻塞
"""

import time

start = time.time()

def hello():
    time.sleep(1)
    print('hello world')

for i in range(10):
    hello()
print(time.time() - start)
