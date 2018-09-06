from selenium import webdriver
import time
import pymongo

client = pymongo.MongoClient("127.0.0.1", connect=False)
db = client["douyu"]




class DouyuSpider:

	def __init__(self):
		self.driver = webdriver.Chrome()
		self.start_url = "https://www.douyu.com/directory/all"

	def parse_url(self):
		li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
		content_list = []
		for li in li_list:
			item = {}
			item["rome_title"] = li.find_element_by_xpath("./a").get_attribute("title")
			item['dy_name'] = li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
			item['rome_tag'] = li.find_element_by_xpath(".//span[@class='tag ellipsis']").text
			item['dy-num'] = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
			item['room_img'] = li.find_element_by_xpath(".//span[@class='imgbox']/img").get_attribute("src")
			print(item)
			content_list.append(item)
		next_url = self.driver.find_elements_by_xpath("//a[@class='shark-pager-next']")

		next_url = next_url[0] if len(next_url) > 0 else None
		return content_list, next_url

	def save_content_list(self,content_list):
		if db["douyu"].insert(content_list):
			print('成功存储到MongoDB', content_list)
			return True
		return False


	def run(self):
		self.driver.get(self.start_url)
		content_list, next_url = self.parse_url()
		self.save_content_list(content_list)
		while next_url is not None:
			next_url.click()
			time.sleep(3)
			content_list, next_url = self.parse_url()
			self.save_content_list(content_list)


if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()