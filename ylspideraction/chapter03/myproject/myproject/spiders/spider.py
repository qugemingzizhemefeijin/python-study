import scrapy
from myproject.items import MyprojectItem

# scrapy crawl dahe
class MySpider(scrapy.Spider):
    # 爬虫名
    name = 'dahe'
    # 文字板块url
    start_urls = ['http://xiaohua.dahe.cn/']
    # 回调函数
    def parse(self, response):
        # 通过xpath提取内容
        contents = response.selector.xpath("//div[@class='media-body']/h4/a/text()").extract()
        # 定义items作为数据暂存容器
        items = MyprojectItem()
        for i in contents:
            items['content'] = i.strip()
            #通过生成器yield将数据传送到pipeline进一步处理
            yield items
        self.log('A response from %s just arrived!' % response.url)