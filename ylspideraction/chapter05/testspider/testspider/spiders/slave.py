from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import redis
import scrapy

# scrapy crawl slavespider
class MySpider(RedisSpider):
    name = 'slavespider' # 爬虫名
    redis_key = 'slave:start_urls' # 读取redis的key
    def make_requests_from_url(self, url):
        print('slave_url:', url) # 打印将要爬取的网页 url
        return None
        #return scrapy.Request(url, callback=self.parse, dont_filter=True)
    def parse(self, response):
        print('slave_url:', response.url) # 打印将要爬取的网页 url
