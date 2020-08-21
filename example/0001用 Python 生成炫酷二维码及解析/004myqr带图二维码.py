# encoding: utf-8

from MyQR import myqr

'''
icture：生成二维码用到的图片
colorized：False 为黑白，True 为彩色
'''

myqr.run(
    words='https://www.baidu.com',
    version=1,
    picture='bg.jpg',
    colorized=True,
    save_name='pmyar.png'
)
