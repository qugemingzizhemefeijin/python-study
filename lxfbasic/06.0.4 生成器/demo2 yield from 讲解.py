"""
如果自己用yield去实现，那只会加大代码的编写难度，降低开发效率，降低代码的可读性。既然Python已经想得这么周到，我们当然要好好利用起来。

讲解它之前，首先要知道这个几个概念

1、调用方：调用委派生成器的客户端（调用方）代码
2、委托生成器：包含yield from表达式的生成器函数
3、子生成器：yield from后面加的生成器函数

你可能不知道他们都是什么意思，没关系，来看下这个例子。

这个例子，是实现实时计算平均值的。
比如，第一次传入10，那返回平均数自然是10.
第二次传入20，那返回平均数是(10+20)/2=15
第三次传入30，那返回平均数(10+20+30)/3=20
"""

# 子生成器
def average_gen():
	total = 0
	count = 0
	average = 0
	while True:
		new_num = yield average
		count += 1
		total += new_num
		average = total/count

# 委托生成器
def proxy_gen():
	while True:
		yield from average_gen()

# 调用方
def main():
	calc_average = proxy_gen()
	next(calc_average)	#预激活下生成器
	print(calc_average.send(10))	#打印：10.0
	print(calc_average.send(20))	#打印：15.0
	print(calc_average.send(30))	#打印：20.0

if __name__ == '__main__':
	main()

"""
认真阅读以上代码，你应该很容易能理解，调用方、委托生成器、子生成器之间的关系。我就不多说了
委托生成器的作用是：在调用方与子生成器之间建立一个双向通道。

所谓的双向通道是什么意思呢？
调用方可以通过send()直接发送消息给子生成器，而子生成器yield的值，也是直接返回给调用方。

你可能会经常看到有些代码，还可以在yield from前面看到可以赋值。这是什么用法？

你可能会以为，子生成器yield回来的值，被委托生成器给拦截了。你可以亲自写个demo运行试验一下，并不是你想的那样。
因为我们之前说了，委托生成器，只起一个桥梁作用，它建立的是一个双向通道，它并没有权利也没有办法，对子生成器yield回来的内容做拦截。

为了解释这个用法，我还是用上述的例子，并对其进行了一些改造。添加了一些注释，希望你能看得明白。

按照惯例，我们还是举个例子。
"""
print('='*20)

# 子生成器
def average_gen2():
	total = 0
	count = 0
	average = 0
	while True:
		new_num = yield average
		if new_num is None:
			break;
		count += 1
		total += new_num
		average = total/count
	# 每一次return，都意味着当前协程结束。
	return total, count, average

# 委托生成器
def proxy_gen2():
	while True:
		 # 只有子生成器要结束（return）了，yield from左边的变量才会被赋值，后面的代码才会执行。
		 total, count, average = yield from average_gen2()
		 print("计算完毕！！\n总共传入 {} 个数值， 总和：{}，平均数：{}".format(count, total, average))

# 调用方
def main2():
	calc_average = proxy_gen2()
	next(calc_average)            # 预激协程
	print(calc_average.send(10))  # 打印：10.0
	print(calc_average.send(20))  # 打印：15.0
	print(calc_average.send(30))  # 打印：20.0
	calc_average.send(None)      # 结束协程
	# 如果此处再调用calc_average.send(10)，由于上一协程已经结束，将重开一协程

if __name__ == '__main__':
	main2()