# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# 导入请求头列表，随机方法，日志
import random
import traceback

from scrapy import signals

from selenium import webdriver
from scrapy.http import HtmlResponse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# process_request
# 在每一个request经过下载中间件的时候被调用。调用结束的时候必须返回None或Response对象或新的Request对象。
# 如果想忽略请求，可以直接使用raise IgnoreRequest。这个IgnoreRequest和Pipeline中的DropItem很像。
# 返回None对象，Scrapy会继续对此request进行处理，执行其他的下载中间件方法，直到download handler下载器处理函数被调用，此request被执行。
# 返回Response对象，Scrapy会停止调用其他的process_request和process_exception方法。因为downloader中间件可以有很多个，在配置中激活，
#    如果其中一个返回了，则其他中间件则不再被调用。
# 返回Request对象，Scrapy会停止调用process_request，重新调度返回的request。
# 返回IgnoreRequest，激活的下载中间件的process_exception会被调用，如果没有处理该异常，request的errback方法也会被调用。
#    但不同其他异常，如果没有对异常进行处理，该异常会被忽略。

# process_response方法同时必须返回Response对象或Request对象或IgnoreRequest异常，不能返回None。
# 返回Response对象，该对象会继续被其他下载中间件中的process_response方法执行。
# 返回Request对象，则会像process_request一样重新调度下载。
# 返回IgnoreRequest，处理process_request。

# process_exception
# 当中间件抛异常的时候，会调用process_exception方法，必须返回Node、Response对象、Request对象中的一个。
# 返回None，其他中间件会继续调用process_exception方法，如果还是没有被处理，则调用默认的异常处理。
# 返回Response对象，重新调用被激活的中间件的process_response方法，不再调用其他中间件。
# 返回Request对象，返回的request对象会被重新下载。

# from_crawler
# 可以为中间件以及Pipeline的运行提供所需的配置参数，通过crawler.settings获得。

# Spider中间件（与下载中间件的区别是，spider中间件是用来处理解析部分的）
# process_spider_input
# 当response经过中间件的时候，调用该方法，处理response对象。process_spider_input应该返回None或者抛出异常。
# 返回None的时候，Scrapy会继续处理response，如果抛出异常会调用process_spider_exception()方法进行处理。

# process_spider_output
# 当Spider处理response返回result的时候，例如爬取获得了item的时候会调用process_spider_output，最后必须返回result。

# process_spider_exception
# process_spider_input抛出异常的时候，调用process_spider_exception进行处理。
# 如果返回None，则会调用其他中间件的process_spider_exception方法。最后异常依旧不被处理，则忽略。

# 当spider发起请求的时候被调用，必须返回一个包含Request对象的可迭代对象。
# 可以用到spider中间件的场景还是比较少的，不过Scrapy内置有几个spider中间件供我们使用并且可以在配置文件settings.py中配置参数。

# DepthMiddleware     追踪request的中间件，用来限制爬取深度。
# HttpErrorMiddleware 过滤出所有失败的请求。http状态码为200-300为成功的请求，其他都做过滤请求，爬虫不再处理那些失败的请求。
#                     如果想处理指定错误的请求，可以在配置文件settings.py中增加HTTPERROR_ALLOWED_CODES来处理 = [404]
# OffsiteMiddleware   这个和爬虫spider属性的allowed_domains相关。会过所有不在allowed_domains范围内的域名。
# RefererMiddleware   referer这个字段一般出现在请求头中，有一些网站会根据referer来判断你的身份。
# UrlLengthMiddleware 用来控制URL的长度，超过指定长度的URL不爬取。
class CustomSpiderMiddleware():
    def process_spider_output(self, response, result, spider):
        raise Exception('CustomSpiderMiddleware.process_spider_output exception')

# Selenium中间件
class SeleniumMiddleware():
    # 当爬虫结束的时候关闭浏览器
    def spider_closed(self, spider):
        self.driver.close()
    # 更换请求方式，使用selenium进行请求，并将结果返回给spider处理
    def process_request(self, request, spider):
        # 更换请求方式，使用selenium进行请求，并将结果返回给spider处理
        try:
            self.driver = webdriver.Chrome()
            self.driver.get(request.url)
            return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8', status=200)
        except Exception:
            # 异常处理，如请求失败则返回状态码500
            traceback.print_exc()
            return HtmlResponse(url=request.url, status=500, request=request)

# 代理ip中间件
class HttpbinProxyMiddleware(object):
    # 从crawler中获取配置
    def __init__(self, crawler):
        self.PROXY = crawler.settings.get('PROXY')
    # 处理request，更换代理
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://' + random.choice(self.PROXY)
        return None
    # 获取crawler实例并返回
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

# 随机User-Agent中间件
class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        # super(RandomUserAgentMiddleware, self).__init__()
        # 获取请求头列表
        self.USER_AGENT_LIST = crawler.settings.get('USER_AGENT_LIST')
    # 使用process_request方法，对request进行修改
    def process_request(self, request, spider):
        # 获取随机请求头
        ua = random.choice(self.USER_AGENT_LIST)
        if ua :
            # 修改请求头UA为随机请求头
            request.headers['User-Agent'] = ua
            spider.logger.info(request.headers['User-Agent'])
        return None
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


class MyprojectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyprojectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
