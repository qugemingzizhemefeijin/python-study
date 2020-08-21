"""
Python对协程的支持是通过generator实现的。

在generator中，我们不但可以通过for循环来迭代，还可以不断调用next()函数获取由yield语句返回的下一个值。

但是Python的yield不但可以返回一个值，它还可以接收调用者发出的参数。

来看例子：

传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。

如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，切换回生产者继续生产，效率极高：
"""

def consumer():
	r = ''
	while True:
		n = yield r
		if not n:
			return
		print('[CONSUMER] Consuming %s...' % n)
		r = '200 OK'

def produce(c):
	c.send(None)
	n = 0
	while n < 5:
		n = n + 1
		print('[PRODUCE] Producing %s...' % n)
		r = c.send(n)
		print('[PRODUCE] Consumer return: %s' % r)
	c.close()

# 获得一个生成器对象
print('running coroutine...V2')
c = consumer()
produce(c)

"""
注意到consumer函数是一个generator，把一个consumer传入produce后：

1.首先调用c.send(None)启动生成器；
2.然后，一旦生产了东西，通过c.send(n)切换到consumer执行；
3.consumer通过yield拿到消息，处理，又通过yield把结果传回；
4.produce拿到consumer处理的结果，继续生产下一条消息；
5.produce决定不生产了，通过c.close()关闭consumer，整个过程结束。

整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。
最后套用Donald Knuth的一句话总结协程的特点：
“子程序就是协程的一种特例。”

在一个生成器函数未启动之前，是不能传递值进去。也就是说在使用c.send(n)之前，必须先使用c.send(None)或者next(c)来返回生成器的第一个值。
"""