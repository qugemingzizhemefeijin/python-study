"""
找一个网页，例如https://www.python.org/events/python-events/，用浏览器查看源码并复制，然后尝试解析一下HTML，输出Python官网发布的会议时间、名称和地点。
"""

from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib import request
from datetime import datetime
from pytz import utc
from pytz import timezone

class EventSearchParser(HTMLParser):

	Cons=[]
	times=[]
	locs=[]
	Conference={'h3':0,'time':0,'span':0}	#FLAG：{'名称':0,'时间':0,'地点':0}

	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)

		if tag == 'h3' and 'class' in attrs:
			if attrs['class'] == 'event-title':
				self.Conference['h3'] = 1
		
		if tag =='time' and 'datetime' in attrs:
			cst_tz = timezone('Asia/Shanghai')
			utc_tz = timezone('UTC')
			dt = datetime.strptime(attrs['datetime'][:-6], '%Y-%m-%dT%H:%M:%S')
			dt_utc = dt.replace(tzinfo=utc_tz)
			dt_sh = dt_utc.astimezone(cst_tz)
			self.times.append('dt_sh')

		if tag == 'span' and 'class' in attrs:
			if attrs['class'] == 'event-location':
				self.Conference['span'] = 1

	def handle_data(self, data):
		if self.Conference['h3'] == 1:
			self.Cons.append(data)
			self.Conference['h3'] = 0
		if self.Conference['span'] == 1:
			self.locs.append(data)
			self.Conference['span'] = 0

def url2html(url):

	with request.urlopen(url) as f:
		html = f.read().decode('utf-8')
	return html

def output(parser):
	i=1
	for x,y,z in zip(parser.Cons, parser.times, parser.locs):
		print('%d ConferencesName:%s\nDate:%s\nLocation:%s\n' % (i,x,y,z))
		i+=1

parser = EventSearchParser()
url = 'https://www.python.org/events/python-events/'
htmlsource = url2html(url)
parser.feed(htmlsource)
output(parser)
