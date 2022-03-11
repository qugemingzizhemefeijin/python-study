"""
字母识别，方法并二值化
"""

from PIL import Image
from pytesser3 import image_to_string
import re

# 打开图片
image = Image.open('img/hoke.png') # 载入图片

# 将图片黑白花
image = image.convert('L')

# 先放大点
image = image.resize((124, 64), Image.BILINEAR)

# 识别图片
vcode = image_to_string(image) # 识别图片
print(vcode)

# 如果识别出乱七八糟的标点符号啥的，可以通过
v = re.findall(r'[a-zA-Z]', vcode)
print(v)
print("".join(v))