"""
通过request获取验证码并解码，这个好像破解不开来。。。无法解析。。但实际上字迹很清晰
"""
import requests
from PIL import Image
from io import BytesIO
from pytesser3 import image_to_string
import random
import re

try:
    url = "http://account.ltaaa.cn/api/verifycode?t=%s" % random.random()
    print(url)
    res = requests.get(url)
    #with open('E:/aaa.jpg','wb') as f:
    #    f.write(res.content)
    #    f.close()
        
    # 打开图片
    image = Image.open(BytesIO(res.content)) # 载入图片
    
    # 将图片黑白花
    image = image.convert('L')
    
    # 先放大点
    image = image.resize((400, 152), Image.BILINEAR)
    
    # 这段代码应该是二值化
    
    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 180
     
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
            
    image = image.point(table, '1')
    
    image.show()

    
    # 识别图片
    vcode = image_to_string(image) # 识别图片
    
    print(vcode)
    
    # 如果识别出乱七八糟的标点符号啥的，可以通过
    v = re.findall(r'[a-zA-Z]', vcode)
    print(v)
    print("".join(v))
except Exception as e:
    print(e)
