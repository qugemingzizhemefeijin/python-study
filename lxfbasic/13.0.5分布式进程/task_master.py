"""
Python的multiprocessing模块不但支持多进程，其中managers子模块还支持把多进程分布到多台机器上。一个服务进程可以作为调度者，将任务分布到其他多个进程中，依靠网络通信。
由于managers模块封装很好，不必了解网络通信的细节，就可以很容易地编写分布式多进程程序。

举个例子：如果我们已经有一个通过Queue通信的多进程程序在同一台机器上运行，现在，由于处理任务的进程任务繁重，希望把发送任务的进程和处理任务的进程分布到两台机器上。怎么用分布式进程实现？

原有的Queue可以继续使用，但是，通过managers模块把Queue通过网络暴露出去，就可以让其他机器的进程访问Queue了。
我们先看服务进程，服务进程负责启动Queue，把Queue注册到网络上，然后往Queue里面写入任务：
"""

import random, queue, time
from multiprocessing.managers import BaseManager

# 发送任务队列
task_queue = queue.Queue()
# 接收结果队列
result_queue = queue.Queue()

#错误：_pickle.PicklingError: Can't pickle <function <lambda> at 0x000001710FDC2EA0>: attribute lookup <lambda> on __main__ failed（pickle模块不能序列化lambda函数）
def return_task_queue():
	global task_queue
	return task_queue

def return_result_queue():
	global result_queue
	return result_queue

# 从BaseManager继承的QueueManager
class QueueManager(BaseManager):
	pass

if __name__ == '__main__':
	# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
	#QueueManager.register('get_task_queue', callable=lambda: task_queue)
	#QueueManager.register('get_result_queue',callable=lambda: result_queue)

	QueueManager.register('get_task_queue', callable=return_task_queue)
	QueueManager.register('get_result_queue',callable=return_result_queue)

	# 绑定端口5000, 设置验证码'abc':
	manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
	# 启动Queue:
	manager.start()

	# 获得通过网络访问的Queue对象:
	task = manager.get_task_queue()
	result = manager.get_result_queue()

	# 放几个任务进去:
	for i in range(10):
		n = random.randint(0, 10000)
		print('Put task %d...' % n)
		task.put(n)

	# 从result队列读取结果...
	print('Try get results...')
	for i in range(10):
		r = result.get(timeout=10)
		print('Result: %s' % r)

	# 关闭:
	manager.shutdown()
	print('master exit.')

"""
请注意，当我们在一台机器上写多进程程序时，创建的Queue可以直接拿来用，但是，在分布式多进程环境下，添加任务到Queue不可以直接对原始的task_queue进行操作，
那样就绕过了QueueManager的封装，必须通过manager.get_task_queue()获得的Queue接口添加。
"""