import scrapy
from myproject.items import MyprojectItem

# scrapy crawl dahetupian
# 下载图片示例
class MySpider2(scrapy.Spider):
    # 爬虫名
    name = 'dahetupian'
    # 图片板块地址
    start_urls = ['http://xiaohua.dahe.cn/2015/9837/104531672/index.html']
    def parse(self, response):
        # 通过xpath提取图片地址
        images = response.selector.xpath("//div[@class='panel-body']/div/img/@src").extract()
        items = MyprojectItem()
        for i in images:
            # url 写入到item中提交，image_urls一定要是列表，如果是字符串会下载失败
            items['image_urls'] = [i.strip()]
            yield items
        self.log('A response from %s just arrived!' % response.url)