"""
yield from 是在Python3.3才出现的语法。所以这个特性在Python2中是没有的。

yield from 后面需要加的是可迭代对象，它可以是普通的可迭代对象，也可以是迭代器，甚至是生成器。

简单应用：拼接可迭代对象#
我们可以用一个使用yield和一个使用yield from的例子来对比看下。

使用yield
"""

# 字符串
astr = 'ABC'
# 列表
alist = [1, 2, 3]
# 字典
adict = {"name": "wangbm", "age": 18}
# 生成器
agen = (i for i in range(4, 8))

def gen(*args, **kw):
	for item in args:
		for i in item:
			yield i

new_list = gen(astr, alist, adict, agen)
print(list(new_list))
#['A', 'B', 'C', 1, 2, 3, 'name', 'age', 4, 5, 6, 7]

#使用yield from

# 生成器
agen = (i for i in range(4, 8))

def gen2(*args, **kw):
	for item in args:
		yield from item

new_list2 = gen2(astr, alist, adict, agen)
print(list(new_list2))

#由上面两种方式对比，可以看出，yield from后面加上可迭代对象，他可以把可迭代对象里的每个元素一个一个的yield出来，对比yield来说代码更加简洁，结构更加清晰。