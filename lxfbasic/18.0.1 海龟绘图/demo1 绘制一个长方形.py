# 导入turtle包的所有内容:

from turtle import *


# 设置笔刷宽度:
width(4)

# 前进：
forward(200)

#右转90度
right(90)

#笔刷颜色
pencolor('red')
forward(100)
right(90)

pencolor('green')
forward(200)
right(90)

pencolor('blue')
forward(100)
right(90)

# 调用done()使得窗口等待被关闭，否则将立刻关闭窗口:
done()

"""
从程序代码可以看出，海龟绘图就是指挥海龟前进、转向，海龟移动的轨迹就是绘制的线条。要绘制一个长方形，只需要让海龟前进、右转90度，反复4次。

调用width()函数可以设置笔刷宽度，调用pencolor()函数可以设置颜色。更多操作请参考turtle库的说明。

绘图完成后，记得调用done()函数，让窗口进入消息循环，等待被关闭。否则，由于Python进程会立刻结束，将导致窗口被立刻关闭。
"""