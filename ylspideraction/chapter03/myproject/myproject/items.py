# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = scrapy.Field()
    # 增加image_urls字段
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    # 下载文件专用
    file_urls = scrapy.Field()
    files = scrapy.Field()
