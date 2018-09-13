# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json
import urllib
from jdbookSpider.items import JdbookspiderItem

class JdSpider(scrapy.Spider):
	name = 'jd'
	allowed_domains = ['jd.com','p.3.cn']
	start_urls = ['https://book.jd.com/booksort.html']
	def parse(self, response):
		dl_list = response.xpath("//div[@class='mc']/dl/dt")
		for dl in dl_list:
			item = JdbookspiderItem()
			item['book_sort'] = dl.xpath("./a/text()").extract_first()
			em_list = dl.xpath("./following-sibling::dd/em")
			for em in em_list:
				item['book_cate'] = em.xpath("./a/text()").extract_first()
				item['book_cate_url'] = em.xpath("./a/@href").extract_first()
				if item['book_cate_url'] is not None:
					item['book_cate_url'] = 'https:' + item['book_cate_url']
				yield scrapy.Request(
					item['book_cate_url'],
					callback=self.parse_cate_url,
					meta={"item": deepcopy(item)}
				)
	def parse_cate_url(self, response):
		item = response.meta["item"]
		li_list = response.xpath("//div[@id='plist']/ul/li")
		for li in li_list:
			item['book_img'] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
			if item['book_img'] is None:
				item['book_img'] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
			item['book_img'] = "https:" + item['book_img'] if item['book_img'] is not None else None
			item['book_name'] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
			item['book_author'] = li.xpath(".//span[@class='author_type_1']/a/text()").extract_first()
			item['publish_time'] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first().strip()
			item['book_store'] = li.xpath(".//span[@class='p-bi-store']/a/@title").extract_first().strip()
			item['book_sku'] = li.xpath("./div/@data-sku").extract_first()
			yield scrapy.Request(
				'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['book_sku']),
				callback=self.parse_book_price,
				meta={"item": deepcopy(item)}
			)
		# 下一页地址构建
		next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
		if next_url is not None:
			print("=========================================")
			next_url = urllib.parse.urljoin(response.url, next_url)
			yield scrapy.Request(
				next_url,
				callback=self.parse_cate_url,
				meta={"item": item}
			)
	def parse_book_price(self, response):
		item = response.meta["item"]
		item['book_price'] = json.loads(response.body.decode())[0]["op"]
		yield item


