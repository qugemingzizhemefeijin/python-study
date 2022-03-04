import scrapy

class MySpider(scrapy.Spider):
    name = "myspider" # 爬虫名称
    start_urls = ["http://example.com", "http://example.org", "http://example.net"]
    # 开始爬取的URL列表
    def parse(self, response):
        if ".org" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self) # 调用parse函数时调用shell