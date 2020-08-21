import functools

#functools.partial就是帮助我们创建一个偏函数的，不需要我们自己定义int2()，可以直接使用下面的代码创建一个新的函数int2：

int2 = functools.partial(int, base=2)

print(int2('1000000'))

#所以，简单总结functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。

#注意到上面的新的int2函数，仅仅是把base参数重新设定默认值为2，但也可以在函数调用时传入其他值

print(int2('1000000', base=10))


"""
最后，创建偏函数时，实际上可以接收函数对象、*args和**kw这3个参数，当传入：

int2 = functools.partial(int, base=2)

实际上固定了int()函数的关键字参数base，也就是：

int2('10010')

相当于：

kw = { 'base': 2 }
int('10010', **kw)
"""

#当传入：
max2 = functools.partial(max, 10)

#实际上会把10作为*args的一部分自动加到左边，也就是：

print(max2(5, 6, 7))

#相当于：
args = (10, 5, 6, 7)
print(max(*args))
