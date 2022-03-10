"""
识别验证码（正确例子，二值化）

7039能识别，7025能识别
"""

from PIL import Image
from pytesser3 import image_to_string

# 打开图片
image = Image.open('img/7025.png') # 载入图片

# 将图片黑白花
image = image.convert('L')

# 这段代码应该是二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
img_out = image.point(table, '1')

# img_out.show()

# 识别图片
vcode = image_to_string(img_out) # 识别图片
print(vcode)
