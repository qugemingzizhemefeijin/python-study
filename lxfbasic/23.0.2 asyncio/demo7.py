"""
在Python3.5中引入的async和await就不难理解了：可以将他们理解成asyncio.coroutine/yield from的完美替身。

当然，从Python设计的角度来说，async/await让协程表面上独立于生成器而存在，将细节都隐藏于asyncio模块之下，语法更清晰明了。 

加入新的关键字 async ，可以将任何一个普通函数变成协程
"""

import time,asyncio,random

async def mygen(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        print(alist.pop(c))
a = ["aa","bb","cc"]
c = mygen(a)
# 输出 <coroutine object mygen at 0x0000019B6E4B5740>
print(c)

"""
但是async对生成器是无效的。async无法将一个生成器转换成协程。 
"""

async def mygen2(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        yield alist.pop(c)
a = ["ss","dd","gg"]
c = mygen2(a)
# 输出 <async_generator object mygen2 at 0x000001F97F8EB4C0>
print(c)

"""
上面例子并不是coroutine协程对象，所以我们的协程代码应该是这样的
"""

async def mygen3(alist):
    while len(alist) > 0:
        c = random.randint(0, len(alist)-1)
        print(alist.pop(c))
        await asyncio.sleep(1)
strlist = ["ss","dd","gg"]
intlist = [1,2,5,6]
c1 = mygen3(strlist)
c2 = mygen3(intlist)
print(c1)

loop = asyncio.get_event_loop()
tasks = [c1, c2]
loop.run_until_complete(asyncio.wait(tasks))
print('All fib finished.')
loop.close()

