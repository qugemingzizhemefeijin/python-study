from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

print(Month.Jan)
print(Month.Jan.name)
#value属性则是自动赋给成员的int常量，默认从1开始计数
print(Month.Jan.value)

#迭代成员
for name, member in Month.__members__.items():
	print(name, '=>', member, ',', member.value)
