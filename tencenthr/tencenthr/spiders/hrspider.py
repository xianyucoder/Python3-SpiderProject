# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from tencenthr.items import TencenthrItem
from urllib import parse
class HrspiderSpider(scrapy.Spider):
    name = 'hrspider'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
        for tr in tr_list:
            item = TencenthrItem()
            item["title"] = tr.xpath("./td[1]/a/text()").extract_first()
            item["position"] = tr.xpath("./td[2]/text()").extract_first()
            item["num"] = tr.xpath("./td[3]/text()").extract_first()
            item["location"] = tr.xpath("./td[4]/text()").extract_first()
            item["publish_date"] = tr.xpath("./td[5]/text()").extract_first()
            url = tr.xpath("./td[1]/a/@href").extract_first()
            item["detail_url"] = parse.urljoin(response.url, url)
            print(item)
            yield scrapy.Request(
                item["detail_url"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        next_url = response.xpath("//a[@id='next']/@href").extract_first()
        if next_url != "javascript:;":
            next_url = "http://hr.tencent.com/" +next_url
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    # 处理详情页
    def parse_detail(self,response):
        item = response.meta["item"]
        job_intrs = response.xpath("//table[@class='tablelist textl']/tr[3]/td/ul/li/text()").extract()
        if job_intrs:
            item["job_intr"] = ",".join(job_intrs)
        else:
            item["job_intr"] ="无"
        job_resps = response.xpath("//table[@class='tablelist textl']/tr[4]/td/ul/li/text()").extract()
        if job_resps:
            item["job_resp"] = ",".join(job_resps)
        else:
            item["job_resp"] = "无"
        print(item)
        yield item