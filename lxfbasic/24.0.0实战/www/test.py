import asyncio, time, os
from functools import cmp_to_key

'''
async def hello(i):
	print('Hello World, %s' % i)
	await asyncio.sleep(1)
	print('Hello Finished, %s' %i)

	print(', '.join('?' for i in range(10)))



loop = asyncio.get_event_loop()
tasks = [hello(1), hello(2)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
'''

async def aaa():
	for i in range(2):
		print(i)
		#time.sleep(1)

async def hello(i):
	print('Hello World, %s' % i)
	await aaa()
	print('========')

x1 = (1, 2, 3)
x2 = ('a', 'b', 'c')

for k, v in zip(x2, x1):
	print('%s=%s' % (k ,v))

a = '1'
b = '2'
c = '3'
print(a+'#'+b+'#'+c)

def yyy(id,name):
	print('id====='+str(id)+',name='+name)

dd = {'id':20,'name':'pp'}
print(yyy(**dd))

print(os.path.abspath('.'))
print(os.path.dirname(__file__))

ss = ['a1','a3','a4','a6','a2']
ss.sort(key=cmp_to_key(lambda s1, s2 : 1 if s1 < s2 else -1))
print(ss)

loop = asyncio.get_event_loop()
tasks = [hello(1),hello(10)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
