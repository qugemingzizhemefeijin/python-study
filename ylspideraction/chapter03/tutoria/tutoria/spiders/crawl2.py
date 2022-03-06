from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_setings

process = CrawlerProcess(get_project_setings())         # 使用项目中的设定
process.crawl('', domain = 'quotes.toscrape.com')       # 可另外添加限制domain
process.start()                                         # 脚本会一直运行直到爬取完成