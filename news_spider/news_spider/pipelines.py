# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class NewsSpiderPipeline(object):
    def open_spider(self,spider):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        self.client = pymongo.MongoClient(host=host, port=port)
        tdb = self.client[dbName]
        tdb.authenticate(name=settings['MONGODB_USER'], password=settings['MONGODB_PASSWD'])
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        spider.log("===========================插入数据| %s |" % item['url'])
        if not self.post.find_one({'url': item['url']}):
            dictitem = dict(item)
            self.post.insert(dictitem)
            return item
        else:
            return DropItem("Duplicate item found: %s" % item)

    def close_spider(self,spider):
        self.client.close()
