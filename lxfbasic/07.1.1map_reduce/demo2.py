from functools import reduce

"""
利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']
"""

def normalize(name):
	return name[:1].upper()+name[1:].lower()

# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)


"""
Python提供的sum()函数可以接受一个list并求和，请编写一个prod()函数，可以接受一个list并利用reduce()求积
"""

def prod(L):
    return reduce(lambda x, y : x * y, L)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')

"""
用map和reduce编写一个str2float函数，把字符串'123.456'转换成浮点数123.456
"""

def str2float(s):
	di = {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
	n = s.index('.')

	def dic(s):
		return di[s]
	
	def re(x, y):
		return x*10+y
	
	return reduce(re, map(dic,s[:n]))+0.1**(len(s)-n-1)*reduce(re,map(dic,s[n+1:]))

print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')