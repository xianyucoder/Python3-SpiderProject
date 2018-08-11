# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencenthrItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    position = scrapy.Field()
    location = scrapy.Field()
    num = scrapy.Field()
    publish_date = scrapy.Field()
    detail_url = scrapy.Field()
    job_resp = scrapy.Field()
    job_intr = scrapy.Field()


class TtItem(scrapy.Item):
    sharetitle = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    num = scrapy.Field()
    duty = scrapy.Field()
    claim = scrapy.Field()