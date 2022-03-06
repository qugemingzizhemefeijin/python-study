import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"                         # 爬虫名
    def start_requests(self):
        urls = [
                'http://quotes.toscrape.com/page/1/',
                'http://quotes.toscrape.com/page/2/'
                ]
        for url in urls :                                           # 发起请求并指定回调函数
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):                                      # 糊掉函数，进行下一步操作
        page = response.url.split("/")[-2]                          # 提取页码
        filename = 'E:/tmp/quotes-%s.html' % page                          # 定义文件名
        with open(filename, 'wb') as f:                             # 建立文件
            f.write(response.body)                                  # 写入爬虫内容
        self.log('Saved file %s' % filename)                        # 打印日志成功保存

# 启动命令 scrapy crawl quotes