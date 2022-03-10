from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import redis
import scrapy

# scrapy crawl masterspider

# 然后录入要抓取的url
# lpush master:start_urls https://wiki.python.org/moin/BeginnersGuide
class MySpider(RedisSpider):
    name = 'masterspider' # 爬虫名
    redis_key = 'master:start_urls' # 读取redis的key
    def __init__(self, *args, **kwargs):
        self.myredis = redis.Redis(host='localhost', port=6379, decode_responses=True) # 初始化连接redis
        super(MySpider, self).__init__(*args, **kwargs)
    def make_requests_from_url(self, url):
        return scrapy.Request(url, callback=self.parse, dont_filter=True)
    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml') # 使用beautifulsoup解析
        for i in soup.find_all('a'): # 找到网页中所有的a元素，获取链接
            try:
                if 'http' not in i.get('href'):
                    print('master_url:', 'https://wiki.python.org' + i.get('href'))
                    self.myredis.lpush('slave:start_urls', 'https://wiki.python.org' + i.get('href')) # 将获取的所有链接存入redis中
            except:
                print('error'.center(50, '*'))
