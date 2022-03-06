import scrapy
from scrapy import crawler
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = "test"                       # 爬虫名
    start_urls = ['http://quotes.toscrape.com/'] # 初始化爬取URL
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
    
process.crawl(MySpider)
process.start()                         # 爬取结束后自动关闭

# python crawl.py