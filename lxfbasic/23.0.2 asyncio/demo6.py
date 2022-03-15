"""
yield from后面接的asyncio.sleep()是一个coroutine(里面也用了yield from)，所以线程不会等待asyncio.sleep()，而是直接中断并执行下一个消息循环。
当asyncio.sleep()返回时，线程就可以从yield from拿到返回值（此处是None），然后接着执行下一行语句。 

asyncio是一个基于事件循环的实现异步I/O的模块。

通过yield from，我们可以将协程asyncio.sleep的控制权交给事件循环，然后挂起当前协程；之后，由事件循环决定何时唤醒asyncio.sleep,接着向后执行代码。 

协程之间的调度都是由事件循环决定。 

yield from asyncio.sleep(sleep_secs) 这里不能用time.sleep(1)因为time.sleep()返回的是None，它不是iterable，还记得前面说的yield from后面必须跟iterable对象(可以是生成器，迭代器)。 
"""
import asyncio,random
@asyncio.coroutine
def smart_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.2)
        yield from asyncio.sleep(sleep_secs) #通常yield from后都是接的耗时操作
        print('Smart one think {} secs to get {}'.format(sleep_secs, b))
        a, b = b, a + b
        index += 1
 
@asyncio.coroutine
def stupid_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.4)
        yield from asyncio.sleep(sleep_secs) #通常yield from后都是接的耗时操作
        print('Stupid one think {} secs to get {}'.format(sleep_secs, b))
        a, b = b, a + b
        index += 1
 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [
        smart_fib(10),
        stupid_fib(10),
    ]
    # asyncio.wait()监听一个协程任务列表
    loop.run_until_complete(asyncio.wait(tasks))
    print('All fib finished.')
    loop.close()
