import scrapy

# 除了使用start_requests()这个函数来开始请求URL，还可以使用更简单的方式，定义一个start_urls列表。
class QuotesSpider(scrapy.Spider):
    name = "quotes2"                         # 爬虫名
    start_urls = [ # 请求URL列表
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/'
    ]
    def parse(self, response):                                      # 糊掉函数，进行下一步操作
        page = response.url.split("/")[-2]                          # 提取页码
        filename = 'E:/tmp/quotes-%s.html' % page                          # 定义文件名
        with open(filename, 'wb') as f:                             # 建立文件
            f.write(response.body)                                  # 写入爬虫内容
        self.log('Saved file %s' % filename)                        # 打印日志成功保存

# 启动命令 scrapy crawl quotes2
# 请求没一个URL返回的response会默认回调到parse()方法中。对入门者来说挺难定位数据的位置。通过shell来学习数据提取是一个不错的选择。
# scrapy shell "http://quotes.toscrape.com/page/1/"
# response.css('title')
# response.css('title::text').extract()  # 只提取文本
# response.css('title').extract()