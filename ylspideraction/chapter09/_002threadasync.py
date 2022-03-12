import time
import threading                        # 多线程模块

start = time.time()                     # 记录开始时间

def hello():
    time.sleep(1)
    print('hello world')

for i in range(0, 10):
    t = threading.Thread(target=hello)  # 创建线程
    t.start()
    
print(time.time() - start)              # 打印使用时间
