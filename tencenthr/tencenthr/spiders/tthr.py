# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencenthr.items import TtItem

class TthrSpider(CrawlSpider):
    name = 'tthr'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    rules = (
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+&keywords=&tid=0&lid=0'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+#a'), follow=True)
    )

    def parse_item(self, response):
        item = TtItem()
        item['sharetitle'] = response.xpath('//td[@id="sharetitle"]/text()').extract_first()
        item['category'] = response.xpath('//span[text()="职位类别："]/../text()').extract_first()
        item['location'] = response.xpath('//span[text()="工作地点："]/../text()').extract_first()
        item['num'] = response.xpath('//span[text()="招聘人数："]/../text()').extract_first()
        item['duty'] = response.xpath('//div[text()="工作职责："]/../ul/li/text()').extract()
        item['claim'] = response.xpath('//div[text()="工作要求："]/../ul/li/text()').extract()
        return item

