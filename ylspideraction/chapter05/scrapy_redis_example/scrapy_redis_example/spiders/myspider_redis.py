import scrapy
from scrapy_redis.spiders import RedisSpider

# 用于整站爬取
# from scrapy.linkextractors import LinkExtractor
# from scrapy_redis.spiders import RedisCrawlSpider

# class MyCrawler(RedisCrawlSpider):

# scrapy crawl myspider_redis
# 另一个终端录入  lpush myspider:start_urls https://www.baidu.com/
class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'myspider:start_urls'
    
    """
    rules = (
        # follow all links
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )
    """

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
        
    def make_requests_from_url(self, url):
        """
                对 request 做一些设置
        :param url:
        :return:
        """
        print("======= %s" % url)
        
        return scrapy.Request(url, callback=self.parse, dont_filter=True)
    
    def make_request_from_data(self, data):
        print("data = %s" % data)
        return self.make_requests_from_url(str(data, encoding='utf-8'))
    
