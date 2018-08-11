# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tencenthr.items import TencenthrItem
from tencenthr.items import TtItem
from pymongo import MongoClient
client = MongoClient()
collection = client["tencent"]["hr1"]

class TencenthrPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TencenthrItem):
            print(item)
            collection.insert(dict(item))
        if isinstance(item, TtItem):
            print(item)
            collection.insert(dict(item))
        return item


# class TtPipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, TtItem):
#             print(item)
#             collection.insert(dict(item))
#         return item