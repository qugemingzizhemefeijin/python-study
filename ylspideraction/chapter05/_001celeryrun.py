from _001celeryHelloWorld import hello
import time

# python _001celeryrun.py

print("=============")
t1 = time.time()

r1 = hello.delay(1, 2)
r2 = hello.delay(2, 4)
r3 = hello.delay(3, 6)
r4 = hello.delay(4, 8)
r5 = hello.delay(5, 10)

r_list = [r1, r2, r3, r4, r5]
for r in r_list:
    while not r.ready():
        pass
    print(r.result)

t2 = time.time()

print('共耗时：%s' % str(t2-t1))

"""
首先，我们一次性调用了五次hello函数，但是运行的总时间才1秒多。这是celery异步运行的结果，如果是同步运行，那么，至少需要5秒多，
因为每调用hello函数一次，就会休眠一秒。这就是celery的强大之处。

从后台输出可以看到，程序会先将任务分发出来，每个任务一个ID，在后台统一处理，处理完后会有相应的结果返回，同时该结果也会储存之后台数据库。
可以利用ready()判断任务是否执行完毕，再用result获取任务的结果。
"""
