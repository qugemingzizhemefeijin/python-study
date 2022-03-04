import scrapy

import requests

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.xpath('span/small/text()').get(),
                'text': quote.css('span.text::text').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
# 运行命令 Scrapy runspider _001spider.py -o quotes.json
# 运行shell scrapy shell "http://baidu.com"

"""
修改请求方式
request = request.replace(method='POST')
response.status
200

引入标准格式化输入模块
from pprint import pprint
pprint(response.headers)

下载完后，url 的内容保存在 response 的变量中
response.body
response.headers
response.headers['Server']
response.xpath() 使用 xpath
response.css() 使用 css 语法选取内容
view(response)  打开浏览器，但是打开的是本地的缓存页面
for i in response.headers:
    print(i)
    
>>> divs = response.xpath("//div")
>>> len(divs)
9
>>> divs[0]
<Selector xpath='//div' data='<div id="wrapper"> <div id="head"> <d...'>

提取内容
divs[1].extract()

获取href的内容
res_href = response.xpath( "//table/tr/td/a/@href" )
for i in res_href :
    print(i.extract())
    
精确查找某个元素
res_href = response.xpath( "//table/tr/td[@id='teacher']" )

"""