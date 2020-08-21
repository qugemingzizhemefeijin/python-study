# encoding:utf-8

'''

'''

from MyQR import myqr

myqr.run(
    words='https://www.baidu.com',
    version=1,
    picture='my.gif',
    colorized=True,
    save_name='myqr.gif'
)
