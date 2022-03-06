# 信号
import scrapy

from scrapy import signals
import time

"""
settings crawler的配置管理器
set(name, value, priority=‘project’)
setdict(values, priority=‘project’)
setmodule(module, priority=‘project’)
get(name, default=None)
getbool(name, default=False)
getint(name, default=0)
getfloat(name, default=0.0)
getlist(name, default=None)
getdict(name, default=None)
copy() # 深拷贝当前配置
freeze()
frozencopy()

signals crawler的信号管理器
connect(receiver, signal)
send_catch_log(signal, **kwargs)
send_catch_log_deferred(signal, **kwargs)
disconnect(receiver, signal)
disconnect_all(signal)

stats crawler的统计信息收集器
get_value(key, default=None)
get_stats()
set_value(key, value)
set_stats(stats)
inc_value(key, count=1, start=0)
max_value(key, value)
min_value(key, value)
clear_stats()
open_spider(spider)
close_spider(spider)

Scrapy内置信号
engine_started        # 引擎启动
engine_stopped        # 引擎停止
spider_opened         # spider开始
spider_idle           # spider进入空闲(idle)状态
spider_closed         # spider被关闭
spider_error          # spider的回调函数产生错误
request_scheduled     # 引擎调度一个 Request
request_dropped       # 引擎丢弃一个 Request
response_received     # 引擎从downloader获取到一个新的 Response
response_downloaded   # 当一个 HTTPResponse 被下载
item_scraped          # item通过所有 Item Pipeline 后，没有被丢弃dropped
item_dropped          # DropItem丢弃item
"""
class delay_test(object):
    def __init__(self, crawler):
        self.crawler = crawler
        # 当收到信号-response_received时，调用方法before_delay
        crawler.signals.connect(self.before_delay, signal = signals.response_received)
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
    # 当response对象的url有pic存在的时候，延迟10秒返回对象
    def before_delay(self, response, spider):
        if 'jpg' in response.url:
            spider.logger.info('爬虫现在延迟10秒，已成功下载%s' % response.url)
            time.sleep(10)
            return response