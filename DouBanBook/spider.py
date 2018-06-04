import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from config import *
from urllib.parse import urlencode
import pymongo
import numpy as np
import time
from faker import Faker
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

fake = Faker()
headers ={	'User-Agent':fake.user_agent()}
tags_index = 'https://book.douban.com/tag'
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
# 请求总标签页https://book.douban.com/tag
def get_tags_index(tags_index):
	try:
		response = requests.get(url=tags_index, headers=headers)
		if response.status_code == 200:
			return response.text
	except RequestException:
		print('请求标签页错误', url)
		return None

# 解析总标签页面,并拼接获得所有标签页页面链接
def splice_tags_indexhtml(html):
	url = 'https://book.douban.com'
	book_tags = []
	tags_url = []
	soup = BeautifulSoup(html, 'lxml')
	tagurl_lists = soup.select('#content > div > div.article > div > div > table > tbody > tr > td > a')
	for tag_url in tagurl_lists:
		# 获取全部标签的a标签内容，并拼接到一起
		book_tags += [tag_url.attrs["href"]]
	for book_tag in book_tags:
		tags_url.append([url + book_tag])
	return tags_url

# 请求tag下的每个页面
def get_tag_page(tag_url,page):
		formdata = {
			'start': page,
			'type': 'T'
		}
		url = tag_url[0]+'?'+ urlencode(formdata)
		try:
			reponse = requests.get(url, headers=headers)
			if reponse.status_code == 200:
				return reponse.text
			return None
		except RequestException:
			print('请求列表页错误')
			return None



# 解析单个tag页面下单页的信息
def parse_tag_page(html):
	try:
		soup = BeautifulSoup(html,"lxml")
		tag_name = soup.select('title')[0].get_text().strip()
		list_soup = soup.find('ul', {'class': 'subject-list'})
		if list_soup == None:
			print('获取信息列表失败')
		else:
			for book_info in list_soup.findAll('div', {'class': 'info'}):
				# 书名
				title = book_info.find('a').get('title').strip()
				# 评价人数
				people_num = book_info.find('span', {'class': 'pl'}).get_text().strip()
				# 出版信息,作者
				pub = book_info.find('div', {'class': 'pub'}).get_text().strip()
				pub_list = pub.split('/')
				try:
					author_info = '作者/译者： ' + '/'.join(pub_list[0:-3])
				except:
					author_info = '作者/译者： 暂无'
				try:
					pub_info = '出版信息： ' + '/'.join(pub_list[-3:-1])
				except:
					pub_info = '出版信息： 暂无'
				try:
					price_info = '价格： ' + '/'.join(pub_list[-1:])
				except:
					price_info = '价格： 暂无'
				try:
					rating_num= book_info.find('span', {'class': 'rating_nums'}).get_text().strip()
				except:
					rating_num = '0.0'
				book_data = {
					'title': title,
					'people_num': people_num,
					'author_info': author_info,
					'pub_info': pub_info,
					'price_info': price_info,
					'rating_num': rating_num
				}
				# return book_data
				if book_data:
					save_to_mongo(book_data,tag_name)
	except:
		print('解析错误')
		return None
# 保存到mongoDB数据库
def save_to_mongo(result,tag_name):
    if db[tag_name].insert(result):
        print('存储到mongoDB成功', result,tag_name)
        return True
    return False



def main():
	tags_indexhtml = get_tags_index(tags_index)
	# 解析并拼接获得全部标签的链接
	tags_url = splice_tags_indexhtml(tags_indexhtml)
	for tag_url in tags_url:
		pages = (x * 20 for x in range(PAGE_START, PAGE_END + 1))
		for page in pages:
			# 请求每一个页面

			tag_html = get_tag_page(tag_url, page)
			time.sleep(np.random.rand() * 50)
			# 解析每一个页面，结构化数据并存储到数据库
			parse_tag_page(tag_html)

if __name__ == '__main__':
    main()