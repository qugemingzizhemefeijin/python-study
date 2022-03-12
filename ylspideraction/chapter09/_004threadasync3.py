import time
import threading

start = time.time()

def sing():
    time.sleep(3)
    print('我喜欢唱歌，现在运行的线程是 %s' % threading.current_thread().name)
    
def dance():
    time.sleep(3)
    print('我喜欢跳舞，现在运行的线程是 %s' % threading.current_thread().name)
    
t1 = threading.Thread(target=sing)
t2 = threading.Thread(target=dance)

t1.start()
t2.start()

t1.join()
t2.join()

print(time.time() - start)
