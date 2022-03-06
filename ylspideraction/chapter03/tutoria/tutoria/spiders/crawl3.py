import scrapy
from scrapy import crawler
from scrapy.crawler import CrawlerProcess

# 在启动scrapy crawl命令时，scrapy默认每个进程运行一个爬虫。但是scrapy支持通过API的方式在一个进程下运行多个爬虫
class MySpider1(scrapy.Spider):                             # 第一个爬虫
    name = 'test1t'
    start_urls = ['http://quotes.toscrape.com/page/1/']
    
class MySpider2(scrapy.Spider):                             # 第二个爬虫
    name = 'test2t'
    start_urls = ['http://quotes.toscrape.com/page/2/']

process = CrawlerProcess()
process.crawl(MySpider1)
process.crawl(MySpider2)
process.start()                         # 爬虫会一直运行直至结束

# 这个案例好像不灵，运行会报错。