import time
import threading

start = time.time()

def hello():
    time.sleep(1)
    print('hello world')

list = []
for i in range(0,10):
    t = threading.Thread(target=hello)
    t.start()
    list.append(t)

# 等待子线程结束
for t in list:
    t.join()
    
print(time.time() - start)
