"""
如果用一个全局dict存放所有的Student对象，然后以thread自身作为key获得线程对应的Student对象如何？

global_dict = {}

def std_thread(name):
    std = Student(name)
    # 把std放到全局变量global_dict中：
    global_dict[threading.current_thread()] = std
    do_task_1()
    do_task_2()

def do_task_1():
    # 不传入std，而是根据当前线程查找：
    std = global_dict[threading.current_thread()]
    ...

def do_task_2():
    # 任何函数都可以查找出当前线程的std变量：
    std = global_dict[threading.current_thread()]
    ...


这种方式理论上是可行的，它最大的优点是消除了std对象在每层函数中的传递问题，但是，每个函数获取std的代码有点丑。
有没有更简单的方式？
ThreadLocal应运而生，不用查找dict，ThreadLocal帮你自动做这件事：
"""

import threading

# 创建全局ThreadLocal对象：

local_school = threading.local()

def process_student():
	# 获取当前线程关联的student
	std = local_school.student
	print('Hello, %s (%s)' % (std, threading.current_thread().name))

def process_thread(name):
	# 绑定ThreadLocal的Student
	local_school.student = name
	process_student()

if __name__ == '__main__':
	t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
	t2 = threading.Thread(target=process_thread, args=('Helen',), name='Thread-B')

	t1.start()
	t2.start()

	t1.join()
	t2.join()

"""
全局变量local_school就是一个ThreadLocal对象，每个Thread对它都可以读写student属性，但互不影响。
你可以把local_school看成全局变量，但每个属性如local_school.student都是线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理。

可以理解为全局变量local_school是一个dict，不但可以用local_school.student，还可以绑定其他变量，如local_school.teacher等等。
ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源。

一个ThreadLocal变量虽然是全局变量，但每个线程都只能读写自己线程的独立副本，互不干扰。ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题。
"""