# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jdbookSpider.items import JdbookspiderItem
from pymongo import MongoClient
client = MongoClient()
collection = client["jdbook"]["book"]


class JdbookspiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JdbookspiderItem):
            print(item)
            collection.insert(dict(item))
        return item
