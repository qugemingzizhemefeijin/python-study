"""
多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，
因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。
来看看多个线程同时操作一个变量怎么把内容给改乱了：
"""

import time,threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
	# 先存后取，结果应该为0:
	global balance
	balance = balance + n
	balance = balance - n

def run_thread(n):
	for i in range(1000000):
		change_it(n)

t1 = threading.Thread(target=run_thread,args=(5,))
t2 = threading.Thread(target=run_thread,args=(8,))

t1.start()
t2.start()

t1.join()
t2.join()

print(balance)

"""
我们定义了一个共享变量balance，初始值为0，并且启动两个线程，先存后取，理论上结果应该为0，但是，由于线程的调度是由操作系统决定的，当t1、t2交替执行时，只要循环次数足够多，balance的结果就不一定是0了。
"""