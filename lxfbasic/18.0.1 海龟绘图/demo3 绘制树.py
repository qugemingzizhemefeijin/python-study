#使用递归，可以绘制出非常复杂的图形。例如，下面的代码可以绘制一棵分型树：

from turtle import *

# 设置色彩模式是RGB:
colormode(255)

lt(90)

lv = 14
l = 120
s = 45

width(lv)

# 初始化RGB颜色:
r = 0
g = 0
b = 0
pencolor(r, g, b)

penup()
bk(l)
pendown()
fd(l)

def draw_tree(l, level):
    global r, g, b
    # save the current pen width
    w = width()

    # narrow the pen width
    width(w * 3.0 / 4.0)
    # set color:
    r = r + 1
    g = g + 2
    b = b + 3
    pencolor(r % 200, g % 200, b % 200)

    l = 3.0 / 4.0 * l

    lt(s)
    fd(l)

    if level < lv:
        draw_tree(l, level + 1)
    bk(l)
    rt(2 * s)
    fd(l)

    if level < lv:
        draw_tree(l, level + 1)
    bk(l)
    lt(s)

    # restore the previous pen width
    width(w)

speed("fastest")

draw_tree(l, 4)

done()



"""
#使用递归，可以绘制出非常复杂的图形。例如，下面的代码可以绘制一棵分型树：

import turtle as tt

def draw_tree(branch_length):
    '''
    绘制分形树函数
    :param branch_length:树枝的长度
    '''
    if branch_length > 5:   #画树枝，直到长度5停止
        # 里层的长度不满足"> 5"后, 就跳出回到上一层（结束条件）

        # 先绘制右侧的树枝
        tt.forward(branch_length)
        # print(f'向前 {branch_length}')
        tt.right(20)
        # print(f'右转 20')
        draw_tree(branch_length-15)

        # 再绘制左侧的树枝
        tt.left(40)
        # print(f'左转 40')
        draw_tree(branch_length-15)

        #返回之前的树枝
        tt.right(20)
        # print(f'右转 20')
        tt.backward(branch_length)
        # print(f'向后 {branch_length}')
        tt.pencolor('brown')
        tt.pensize(2)
    else:
        tt.color('green')    # 画末端
        tt.pensize(4)


def draw():
    '''
        调用绘制分形树
    '''
    # 初始化画树的位置及笔宽
    tt.left(90)
    tt.penup()
    tt.backward(200)
    tt.pendown()
    tt.pencolor('brown')
    tt.pensize(2)
    draw_tree(100)

    tt.exitonclick()

if __name__ == '__main__':
    tt.speed(10)  # 最快的速度
    draw()
"""