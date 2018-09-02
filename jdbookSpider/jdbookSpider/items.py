# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbookspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_sort = scrapy.Field()
    book_cate = scrapy.Field()
    book_cate_url = scrapy.Field()
    book_img = scrapy.Field()
    book_name = scrapy.Field()
    book_author = scrapy.Field()
    publish_time = scrapy.Field()
    book_store = scrapy.Field()
    book_sku = scrapy.Field()
    book_price = scrapy.Field()
