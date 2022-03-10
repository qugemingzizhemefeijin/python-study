"""
识别验证码（正确例子，但是还是有问题，只能解决部分问题）

7039能识别，7025无法识别
"""

from PIL import Image
from pytesser3 import image_to_string

# 打开图片
image = Image.open('img/7025.png') # 载入图片

# 将图片黑白花
image = image.convert('L')

# 识别图片
vcode = image_to_string(image) # 识别图片
print(vcode)
