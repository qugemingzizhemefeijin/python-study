"""
继承
"""

import time
import threading

start = time.time()

class myThread(threading.Thread):
    def __init__(self, threadID, name, delay, hobby):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.delay = delay
        self.hobby = hobby
    def run(self):
        print('开始线程：' + self.name)
        foo(self.name, self.delay, self.hobby)
        print('退出线程：' + self.name)
    
def foo(threadName, delay, hobby):
    time.sleep(delay)
    print(f'这里是{threadName}，睡眠{delay}秒，我喜欢{hobby}')

# 创建线程
thread1 = myThread(1, 'Thread-1', 1, '唱歌')
thread2 = myThread(2, 'Thread-2', 2, '跳舞')

thread1.start()
thread2.start()

thread1.join()
thread2.join()

end = time.time() - start
print('退出主线程')
print(f'花费时间{end}秒')
