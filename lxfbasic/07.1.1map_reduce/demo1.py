from functools import reduce

"""
map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回

"""

def f(x):
	return x*x

r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
print(list(r))

#也可以这样实现
L = []
for n in range(9):
	L.append(f(n+1))

print(list(L))

print(list(map(str, range(10))))


#####reduce
"""
reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
"""

def add(x, y):
	return x+y

print(reduce(add, [1, 3, 5, 7, 9]))

"""
当然求和运算可以直接用Python内建函数sum()，没必要动用reduce
但是如果要把序列[1, 3, 5, 7, 9]变换成整数13579，reduce就可以派上用场
"""

def fn(x, y):
	return x*10 + y

print(reduce(fn, [1, 3, 5, 7, 9]))

"""
这个例子本身没多大用处，但是，如果考虑到字符串str也是一个序列，对上面的例子稍加改动，配合map()，我们就可以写出把str转换为int的函数
"""
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def char2num(s):
	return DIGITS[s]

print(reduce(fn, map(char2num, '13579')))

#整理成一个str2int的函数就是

def str2int(s):
	def fn(x,y):
		return x*10 + y
	def char2num(s):
		return DIGITS[s]
	return reduce(fn, map(char2num, s))

print(str2int('13579'))


#还可以用lambda函数进一步简化成

def str3int(s):
	return reduce(lambda x, y : x * 10 + y, map(char2num, s))

print(str3int('14968'))