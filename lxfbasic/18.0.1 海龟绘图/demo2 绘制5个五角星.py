#turtle包本身只是一个绘图库，但是配合Python代码，就可以绘制各种复杂的图形。例如，通过循环绘制5个五角星：

from turtle import *

def drawStar(x, y):
	pu()
	goto(x, y)
	pd()
	# set heading: 0
	seth(0)
	for i in range(5):
		fd(40)
		rt(144)

for x in range(0, 250, 50):
	drawStar(x, 0)


done()
