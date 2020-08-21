# encoding: utf-8
"""
安装源有问题，可以用以下命令直接读取国内源
pip install -i https://pypi.douban.com/simple 包名

爬虫-拉勾招聘需求词频分析

https://www.jianshu.com/p/16cd37a5355f


MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors
需要将

import gevent
from gevent import monkey
monkey.patch_all()
import requests       #导入顺序，否则会报错
"""

import json
import time
import gevent
from gevent import monkey
from setting import *
from HandleData import handle
from lxml import etree
from queue import Queue
from wordcloud import WordCloud, STOPWORDS

monkey.patch_all()	# 用于将标准库中大部分阻塞式调用修改为协作式运行

import requests


# 主爬虫类
class LagouCrawl(object):

	# 初始化数据，传入城市和关键词
	def __init__(self, city, keyword):
		# 创建一个session，主要是用于请求的时候保持session或cookie
		self.session = requests.session()
		self.queue = Queue()
		self.keyword = keyword
		# 存储的文件名由 城市-关键词.txt 命令
		self.filename = city + '-'+keyword+'.txt'
		# 构建查询字符串参数
		self.params = {
			'needAddtionalResult': False,
			'isSchoolJob': 0
		}
		# 如果没有 city 字段默认查询全国的职位，有则加上相应城市
		if city != '全国':
			self.params['city'] = city

	# 构建表单数据，传入页page，使用关键词
	def get_data(self, page):
		data = {
			"first": "false",
			"pn": page,
			"kd": self.keyword
		}

		return data

	# 请求json数据
	def post_api(self, data):
		res = self.session.post(API_URL, headers=HEADERS, data=data, params=self.params, verify=False)
		res.encoding = 'utf-8'
		return res.text

	# 构建详情页的url,放入队列
	def build_detail_url(self, data, num):
		for i in range(num):
			position_id = data['content']['positionResult']['result'][i]['positionId']
			url = INFO_URL % position_id
			self.queue.put(url)

	# 爬取json数据的爬虫
	def lagou_spider(self):
		page = 1
		# 剩余数量计数
		rest_count = 0
		while True:
			# 获取表单数据
			data = self.get_data(page)
			# 把数据传入，发起请求
			text = self.post_api(data)
			print(text)
			# 把得到的json数据转成字典
			data = json.loads(text)
			# 当前页的岗位数据量
			num = data['content']['positionResult']['resultSize']
			# 所有结果的总数量
			total_count = data['content']['positionResult']['totalCount']

			if page == 1:
				rest_count = total_count
			rest_count = rest_count - num

			# 构建url
			self.build_detail_url(data, num)

			print('第%d页' % page)
			print('招聘总数:', total_count)
			print('本页数量:', num)
			print('剩余数量:', rest_count)

			# 剩余数量小于等于0，退出这个任务
			if rest_count <= 0:
				break

			# 翻页
			page += 1
			# 休眠40秒
			time.sleep(40)

	# 爬取详情页的爬虫
	def get_info(self):
		# 计数：已完成的个数
		count = 0
		while True:
			try:
				count += 1
				# 从队列拿出url发起请求
				url = self.queue.get()
				html = self.get_html(url)
				info_text = self.parse_html(html)
				print(info_text)
				# 保存数据到文件
				self.save_data(info_text)
				print("已完成:%d, url:%s" % (count, url))
				# 队列任务减一
				self.queue.task_done()
			except Exception as e:
				print(e)

			time.sleep(25)

	# 详情页请求
	def get_html(self, url):
		res = requests.get(url, headers=HEADER)
		res.encoding = 'utf-8'
		return res.text

	# 解析详情页，获得数据
	def parse_html(self, html):
		obj_xpath = etree.HTML(html)
		node = obj_xpath.xpath("//dd[@class='job_bt']")
		info_node = node[0]
		info_text = info_node.xpath('string(.)').strip()
		return info_text

	# 保存数据
	def save_data(self, data):
		with open(self.filename, 'a', encoding='utf-8') as f:
			f.write(data)

	# 开始爬取
	def start_crawl(self):
		# 开启一个协程爬 获取json数据，构建详情页 url
		g1 = gevent.spawn(self.lagou_spider)
		time.sleep(5)
		# 开启一个协程爬详情页的数据，进行保存
		g2 = gevent.spawn(self.get_info)
		# 队列阻塞，直到队列任务完成
		self.queue.join()

# 获得城市列表
class CityInfo(object):

	def __init__(self):
		self.url = 'https://www.lagou.com/jobs/allCity.html'

	# 获得城市列表
	def get_city(self):
		response = requests.get(self.url, headers=HEADERS)
		response.encoding = 'utf-8'
		html = response.text
		xpath_obj = etree.HTML(html)
		city_list = xpath_obj.xpath('//ul[@class="city_list"]/li/a/text()')

		return city_list


if __name__ == '__main__':
	print('程序开始!')
	city_info = CityInfo()
	city_list = city_info.get_city()
	# 在城市列表中加入 全国
	city_list.append('全国')
	city = input('请输入要查询的城市(查询全国输入 全国 ):')
	# 输入城市在列表内则输入关键字，否则结束。
	if city in city_list:
		keyword = input('请输入要查询的关键词:')
		spider = LagouCrawl(city, keyword)
		# 开启爬虫
		spider.start_crawl()
		# 默认停用词与自定义的取并集
		stop = STOPWORDS | STOPWORD_NEW
		# 调用数据处理
		handle(city + '-' + keyword + '.txt', stop)
	else:
		print('输入城市不存在')
	print('程序执行完毕')