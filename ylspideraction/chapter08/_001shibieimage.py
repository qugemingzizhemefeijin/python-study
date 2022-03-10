"""
识别字母
"""

from PIL import Image
from pytesser3 import image_to_string

image = Image.open('E:/20220310211734.jpg') # 载入图片
# 打开图片
image.show()

vcode = image_to_string(image) # 识别图片
print(vcode)
