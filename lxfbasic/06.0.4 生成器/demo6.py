"""
for n in range(1000):
    a=n
    
这个时候range(1000)就默认生成一个含有1000个数的list了，所以很占内存。
这个时候你可以用刚才的yield组合成生成器进行实现，也可以用xrange(1000)这个生成器实现。
"""

def foo(num):
    print("starting...")
    while num<10:
        num=num+1
        yield num
for n in foo(0):
    print(n)
    
"""
其中要注意的是python3时已经没有xrange()了，在python3中，range()就是xrange()了。
"""    
for n in range(1000):
    print(n)
    