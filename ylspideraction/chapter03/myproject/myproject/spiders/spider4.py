import scrapy
from myproject.items import MyprojectItem

# scrapy crawl daheua
# 随机修改User-Agent示例
class MySpider4(scrapy.Spider):
    # 爬虫名
    name = 'daheua'
    # 图片板块地址
    start_urls = ['http://xiaohua.dahe.cn/2015/9837/104531672/index.html']
    def parse(self, response):
        # 通过xpath提取图片地址
        images = response.selector.xpath("//div[@class='panel-body']/div/img/@src").extract()
        items = MyprojectItem()
        for i in images:
            # url 写入到item中提交
            items['image_urls'] = [i.strip()]
            # yield items
            # 取消yield items，对每一个图片url发送请求，结果返回到函数parse_image中
            yield scrapy.Request(url=items['image_urls'][0], callback=self.parse_image)
        # self.log('A response from %s just arrived!' % response.url)
    def parse_image(self, response):
        # 访问图片成功后，会在控制台打印日志
        self.log('这里是%s' % response.url)
        self.log('A response from %s just arrived!' % response.url)
