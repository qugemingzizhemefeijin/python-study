# Scrapy settings for myproject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# 爬虫名称
BOT_NAME = 'myproject'
# 爬虫模块（编写爬虫爬取逻辑的所在。）
SPIDER_MODULES = ['myproject.spiders']
NEWSPIDER_MODULE = 'myproject.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'myproject (+http://www.yourdomain.com)'

# 机器人守则（robots.txt规则）
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 控制下载并发数，默认为16个并发。如果完成一次请求需要的时间是0.25，16个并发每秒会产生64个请求。
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#下载延迟。爬虫爬取的过程是一个不断向目标网站发起请求的过程，过快的爬取速度则会给对方服务器造成负担，变成一种攻击行为。
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# 对单个网站进行并发请求的最大值
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 对单个IP进行并发请求的最大值，这个设定为非0的时候，DOWNLOAD_DELAY延迟作用在IP上而不是网站。
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 默认使用的请求头，爬虫伪装最简单的手段，伪装请求头。
# 这里会发现请求头中没有USER_AGENT，那是因为scrapy基本配置有着独立的USER_AGENT参数。
# USER_AGENT = 'myproject (+http://www.yourdoman.com)'
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   'User-Agent': '"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5"',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'myproject.middlewares.MyprojectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'myproject.middlewares.MyprojectDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# item是一个存放数据的容器，通过items.py进行定义。然后爬虫模块通过import进行使用。
# 但是最后数据流转到哪个模块中进行清洗或者保存，需要在ITEM_PIPELINES中进行配置。
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 这里 myproject.pipelines.MyprojectPipeline 指在myproject项目中pipelines模块中的MyprojectPipeline类需要使用到item，
# 后面的数字500代表优先级，数字越小优先级越高。
ITEM_PIPELINES = {
    # 如果新建了一个pipelines，这里就需要添加上如 'myproject.pipelines.newPipeline': 350
    # 'myproject.pipelines.MyprojectPipeline': 300,
    # 'myproject.pipelines.MyImagesPipeline': 300,
    # 专门下载文件
    'scrapy.pipelines.files.FilesPipeline': 1,
}

# ImagesPipeline 的设置
IMAGES_STORE = 'E:/tmp/images' # 图片保存地址
# 过期天数
IMAGES_EXPIRES = 90 # 90天内抓取的都不会被重抓
# 缩略图的尺寸，设置这个值就会产生缩略图 （图片最后保存的时候是等比例缩放的）
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (200, 200),
}

# 不符合图片尺寸要求的小图，会被过滤，不再下载
# IMAGES_MIN_WIDTH = 800          # 最小宽度
# IMAGES_MIN_HEIGHT = 640         # 最小高度

# 下载文件保存路径
FILES_STORE = "E:/tmp/downloadfile"

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MONGO_URI = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DB = 'test'

