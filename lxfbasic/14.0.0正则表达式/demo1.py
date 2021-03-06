import re

###re模块

#<re.Match object; span=(0, 9), match='010-12345'>
print(re.match(r'^\d{3}\-\d{3,8}$', '010-12345'))
#None
print(re.match(r'^\d{3}\-\d{3,8}$', '010 12345'))

#match()方法判断是否匹配，如果匹配成功，返回一个Match对象，否则返回None。常见的判断方法就是：

test = '用户输入的字符串'
if re.match(r'正则表达式', test):
	print('OK')
else:
	print('failed')

###切分字符串

#用正则表达式切分字符串比用固定的字符更灵活，请看正常的切分代码：

#['a', 'b', '', '', 'c']
print('a b   c'.split(' '))

#嗯，无法识别连续的空格，用正则表达式试试：

#['a', 'b', 'c']
print(re.split(r'\s+', 'a b   c'))

#无论多少个空格都可以正常分割。加入,试试：
#['a', 'b', 'c', 'd']
print(re.split(r'[\s\,]+', 'a,b, c  d'))

#再加入;试试：
#['a', 'b', 'c', 'd']
print(re.split(r'[\s\,\;]+', 'a,b;; c  d'))

###分组

"""
除了简单地判断是否匹配之外，正则表达式还有提取子串的强大功能。用()表示的就是要提取的分组（Group）。比如：

^(\d{3})-(\d{3,8})$分别定义了两个组，可以直接从匹配的字符串中提取出区号和本地号码：
"""

m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print(m)

print(m.group(0))
print(m.group(1))
print(m.group(2))

t = '19:05:30'
m1 = re.match(r'^(0[0-9]|1[0-9]|2[0-3]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])\:(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9])$', t)
#获取元祖
print(m1.groups())

###贪婪匹配

#最后需要特别指出的是，正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符。举例如下，匹配出数字后面的0：
print(re.match(r'^(\d+)(0*)$', '102300').groups())
#('102300', '')

#由于\d+采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了。
#必须让\d+采用非贪婪匹配（也就是尽可能少匹配），才能把后面的0匹配出来，加个?就可以让\d+采用非贪婪匹配：

print(re.match(r'^(\d+?)(0*)$', '102300').groups())
#('1023', '00')

###编译

"""
当我们在Python中使用正则表达式时，re模块内部会干两件事情：

编译正则表达式，如果正则表达式的字符串本身不合法，会报错；

用编译后的正则表达式去匹配字符串。

如果一个正则表达式要重复使用几千次，出于效率的考虑，我们可以预编译该正则表达式，接下来重复使用时就不需要编译这个步骤了，直接匹配：
"""

# 编译:
re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
# 使用
print(re_telephone.match('010-12345').groups())
#('010', '12345')
print(re_telephone.match('010-8086').groups())
#('010', '8086')

#编译后生成Regular Expression对象，由于该对象自己包含了正则表达式，所以调用对应的方法时不用给出正则字符串。

