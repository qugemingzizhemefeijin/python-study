# 接上一个列子
# 我们用Task封装两个coroutine试试：

import threading
import asyncio

@asyncio.coroutine
def hello():
	print('Hello World! (%s)' % threading.currentThread())
	yield from asyncio.sleep(1)
	print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()

#由打印的当前线程名称可以看出，两个coroutine是由同一个线程并发执行的。