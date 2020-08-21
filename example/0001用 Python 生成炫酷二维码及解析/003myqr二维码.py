# encoding: utf-8
'''
如果我们对上面生成二维码的样式不满意，我们就需要用到 myqr 库了，它不仅可以生成普通二维码，
还可以生成带图片的二维码以及动态二维码，但我们想要查看生成的二维码时，需要到保存位置手动打开查看。
'''

from MyQR import myqr

'''
words：内容
version：容错率
save_name：保存的名字
'''

myqr.run(
    words='https://www.baidu.com',
    version=1,
    save_name='myqr.png'
)
