# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# 引入ImagesPipeline这个类
from scrapy.pipelines.images import ImagesPipeline
# 引入DropItem，发生异常时抛弃item
from scrapy.exceptions import DropItem
import pymongo

# 这里要注意，必须要在settings.py中激活ITEM_PIPELINES
class MyprojectPipeline:
    #这个函数就是实例化Spider类最终函数，cls()调用（其实就是构造函数）
    def __init__(self, mongouri, mongoport, mongodb):
        # 这里将mongodb的链接属性设置到self中
        self.mongouri = mongouri
        self.mongoport = mongoport
        self.mongodb = mongodb
    # @classmethod表示该方法输入该类，可以直接由类名调用，不必通过对象调用
    # 即Spider.from_crawler(crawler)即可调用该函数。在Crawler类中，Crawler通过
    # 传入一个Spider类作为参数初始化该Crawler，这个Spider类直接调用该from_crawler()
    # 函数从而实现Spider的初始化。
    @classmethod
    def from_crawler(cls, crawler):
        # 实例化MyprojectPipeline这个对象
        return cls(
            mongouri = crawler.settings.get('MONGO_URI'),
            mongoport = crawler.settings.get('MONGO_PORT'),
            mongodb = crawler.settings.get('MONGO_DB')
        )
    # 处理提取的数据(保存数据)
    def process_item(self, item, spider):
        # 打开文件data.json，如果没有则创建
        # f = open('E:/tmp/data.json', 'a')
        #写入数据
        # f.write(str(item) + ',\n')
        # f.close()
        # return item
        self.db["test"].insert_one(dict(item))
        return item
    # 开启爬虫时执行，只执行一次
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
                        host=self.mongouri,
                        port=self.mongoport,
                        username="root",
                        password="123456",
                        authSource="test",
                        authMechanism='SCRAM-SHA-1')
        self.db = self.client[self.mongodb]
    # 关闭爬虫时执行，只执行一次。
    # 如果爬虫中间发生异常导致崩溃，close_spider可能也不会执行
    def close_spider(self, spider):
        self.client.close()

# 下载图片的pipeline处理
class MyImagesPipeline(ImagesPipeline):
    # get_medis_requests方法从item中获取url进行下载
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)
    # 当下载完成时，调用item_completed方法，保存图片
    def item_completed(self, results, item, info):
        # 判断有没有图片path这个值，OK代表有，存储到 image_paths 项目组中，如果其中没有图片，则抛出异常
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            # 当没有返回图片路径时，抛弃item，在调用spider3的时候这里应该会报错。。所以在调式spider3代码的时候，在settings中注释掉此pipeline
            raise DropItem("Item contains no images")
        # 将图片本地路径写入item
        item['image_paths'] = image_paths
        return item
    
    