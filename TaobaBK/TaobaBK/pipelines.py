# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

from scrapy.conf import settings
from scrapy.exceptions import DropItem

class TaobabkPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER_IP'],
            settings['MONGODB_SERVER_PORT']
        )

        db = connection[settings['MONGODB_DB_NAME']]
        self.collection = db[settings['MONGODB_COLLECTION']]

        #Empty the collections here on demand

    def process_item(self, item, spider):

        if 'goods_name' not in item:
            raise DropItem("Invalid Data without goods name")
        elif len(item['goods_name']) == 0:
            raise DropItem("Invalid Data with empty goods name")
        else:
            self.collection.insert(dict(item))

        return item