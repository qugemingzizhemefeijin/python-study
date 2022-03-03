"""
给res赋值
"""
def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)
g = foo()
print(next(g))
print("*"*20)
print(g.send(7))

"""
starting...
4
********************
res: 7
4
"""

"""
send是发送一个参数给res的，因为上面讲到，return的时候，并没有把4赋值给res，下次执行的时候只好继续执行赋值操作，只好赋值为None了，
而如果用send的话，开始执行的时候，先接着上一次（return 4之后）执行，先把7赋值给了res,然后执行next的作用，遇见下一回的yield，return出结果后结束。


5.程序执行g.send(7)，程序会从yield关键字那一行继续向下运行，send会把7这个值赋值给res变量；
6.由于send方法中包含next()方法，所以程序会继续向下运行执行print方法，然后再次进入while循环；
7.程序执行再次遇到yield关键字，yield会返回后面的值后，程序再次暂停，直到再次调用next方法或send方法。
"""