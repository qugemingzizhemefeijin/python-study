"""
PIL：Python Imaging Library，已经是Python平台事实上的图像处理标准库了。PIL功能非常强大，但API却非常简单易用。

由于PIL仅支持到Python 2.7，加上年久失修，于是一群志愿者在PIL的基础上创建了兼容的版本，名字叫Pillow，支持最新Python 3.x，又加入了许多新特性，因此，我们可以直接安装使用Pillow。

安装Pillow
如果安装了Anaconda，Pillow就已经可用了。否则，需要在命令行下通过pip安装：

$ pip install pillow
如果遇到Permission denied安装失败，请加上sudo重试。
"""

###操作图像

#来看看最常见的图像缩放操作，只需三四行代码：

from PIL import Image, ImageFilter

# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
#获得图像尺寸:
w, h = im.size
print('Original image size: %sx%s' %(w, h))
# 缩放到50%:
im = im.resize((w//2, h//2), Image.ANTIALIAS)
print('Resize image to:%sx%s' %(w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
im.save('thumbnail.jpg', 'jpeg')

#其他功能如切片、旋转、滤镜、输出文字、调色板等一应俱全。
#比如，模糊效果也只需几行代码：

im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.jpg', 'jpeg')
