"""
识别验证码（错误例子）

7039能识别，7025无法识别
"""

from PIL import Image
from pytesser3 import image_to_string

# 打开图片
image = Image.open('img/7025.png') # 载入图片

# 识别图片
vcode = image_to_string(image) # 识别图片
print(vcode)
