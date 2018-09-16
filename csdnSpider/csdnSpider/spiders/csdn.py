# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver

class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['https://passport.csdn.net/account/login','https://i.csdn.net/#/account/index']

    def __init__(self):
        # mobilsetting = {"deviceName":"iPhone 6 Plus"}
        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("mobileEmulation", mobilsetting)
        self.browser = None
        self.cookies = None
        # self.browser.set_window_size(400,800)
        super(CsdnSpider, self).__init__()
    def spider_closed(self, response):
        print("spider close")
        self.brower.close()


    def parse(self, response):
        print(response.url)
        print(response.body.decode("utf-8","ignore"))