#encoding:utf-8

#https://mp.weixin.qq.com/s?__biz=MzI4NDY5Mjc1Mg==&mid=2247490895&idx=2&sn=00f375ede7c9412fa8c1c6f2ca88b6fc&chksm=ebf6c530dc814c264a1554bb0992621cf251124a64b694f3faedd7e8dbad5b067e29802876db&scene=126&sessionid=1583293673&key=f1120516e6597816f0abb5563be33c7239b43196519353fcac28c2a3d41536df638c25ca8102bd3ccc655d347d2e4933fbe0ae2d277fc9affd88079d254dedbc66c26ab1ebc7c96f8d82effececc7bdf&ascene=1&uin=ODY4Mjc0OTA3&devicetype=Windows+10&version=62080079&lang=zh_CN&exportkey=A%2FWWn%2FFnMU%2B164dAw9L5CLc%3D&pass_ticket=od4XohbhAaD%2BNFYR0cEbFkqZk%2BIVdqHKtpp%2FA9LfdakILuM79mk1YVmbpBAycNOP

"""
言归正传，对于一个热衷技术且大有前途的青年来说，数据看久了是不是想到要展示一个技术大白的真正技术了呢？今天的文章主人翁就抱着学习的态度将腾讯每天推送的实时疫情数据爬取下来进行数据展示。

思路：

网页分析
实时数据抓取
数据可视化展示

在百度中搜索 https://news.qq.com/zt2020/page/feiyan.htm 即可获得疫情实时追踪展示信息
"""

import time, json, requests

# 使用 Matplotlib 绘制全国确诊病例柱状图
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  #正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    #正常显示负号

# 腾讯疫情实时数据数据 URL
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
# 加载 JSON 数据并解析
data = json.loads(requests.get(url=url).json()['data'])

# 打印数据
# print(data)
print(data.keys())

# 统计省份信息(34个省份 湖北 广东 河南 浙江 湖南 安徽....)
num_area = data['areaTree'][0]['children']
print(len(num_area))

# 遍历所有数据后输出，直到输出结束
for item in num_area:
	print(item['name'],end=' ')
else:
	print('\n')

# 解析所有确诊数据
all_data = {}
for item in num_area:
	# 输出省市名称
	if item['name'] not in all_data:
		all_data.update({item['name']:0})
	# 输出省市对应的数据
	for city_data in item['children']:
		all_data[item['name']] += int(city_data['total']['confirm'])

# 输出结果
print(all_data)

#获取数据
names = all_data.keys()
nums = all_data.values()
print(names)
print(nums)

# 绘图
plt.figure(figsize=[11,7]) # 定义图片大小和长宽
# 绘制图形
plt.bar(names, nums, width=0.8, color='purple')

# 设置标题
plt.xlabel("地区", fontproperties='SimHei', size=15)
plt.ylabel("人数", fontproperties='SimHei', rotation=90, size=12)
plt.title("全国疫情确诊图", fontproperties='SimHei', size=16)
# 展示x轴的每项名称，并且旋转-60度等
plt.xticks(list(names), fontproperties='SimHei', rotation=-60, size=10)

# 显示数字（）
for a, b in zip(list(names), list(nums)):
	# args1 = x坐标,args2 = x值, args3 = 显示的字符串
	plt.text(a, b, b, ha='center', va='bottom', size=6)

# 图形展示
plt.show()