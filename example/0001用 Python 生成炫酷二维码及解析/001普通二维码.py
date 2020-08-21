# encoding:utf-8
'''
https://mp.weixin.qq.com/s?__biz=MzU1NDk2MzQyNg==&mid=2247484874&idx=1&sn=f126311f189e8d53be265a2e257abc66&chksm=fbdadd47ccad5451caf0952747cd2c5debe87a56ed1ed2ec08b06100b853fb13d32baed4bcbd&mpshare=1&scene=1&srcid=&sharer_sharetime=1585322686655&sharer_shareid=ce1c9240f8bf63dd6856d9d376f3f906&key=68d3afa56a8f7776c4007a28bf9300114012e081f47889ed074f1d68a53fc5dedccd2898568cc5cff8fc5cf31ff2f1167ac5b5f46f5d09b2bccf5a6f2ef632746182954782522994ed5bac9dfd04f1f7&ascene=1&uin=ODY4Mjc0OTA3&devicetype=Windows+10&version=62090045&lang=zh_CN&exportkey=AzIzryFVVHGFMzMy4vJ0lXs%3D&pass_ticket=ZZqhUuDWzW0IyYFgnRqbxhOKd%2B%2F12rlEuzRCK4t8r1rS3pUzg5gbY4XlHmnhCy5x

用 Python 生成炫酷二维码及解析
'''
import qrcode

# 二维码内容
data = 'https://www.baidu.com'
# 生成二维码
img = qrcode.make(data=data)
# 显示二维码
img.show()
# 保存二维码
img.save('ar.jpg')
