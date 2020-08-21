"""
用asyncio提供的@asyncio.coroutine可以把一个generator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。

请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：


@asyncio.coroutine
def hello():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")
"""

import asyncio

async def hello():
	print('Hello world!')
	r = await asyncio.sleep(1)
	print('Hello again!')

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([hello(), hello()]))
loop.close()
