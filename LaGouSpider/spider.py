import requests
from requests.exceptions import RequestException
import json
from urllib.parse import urlencode
import pymongo
import numpy as np
import time
from config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

# headers = {
# 	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# 	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
# 	'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
# }
# 构建headers,从这个列表里随机获取header
hds = [{
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
	'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=false&suginput=',
},{	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
	'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
},{	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=false&suginput=',
},{	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
	'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=false&suginput=',
},{	'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=false&suginput=',
},{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=false&suginput=',
}]


# 构建请求链接
def make_url(page):
	formdata = {
		'needAddtionalResult': 'false',
		'first': 'true',
		'pn': page,
		'kd': 'python'
	}
	url = u'https://www.lagou.com/jobs/positionAjax.json?' + urlencode(formdata)
	return url

# 构建每一页的链接
def get_index_page(url,page):
	try:
		reponse = requests.get(url, headers=hds[page%len(hds)])
		if reponse.status_code == 200:
			return reponse.text
		return None
	except RequestException:
		print('请求职位列表页错误')
		return None

# 解析列表页
def parse_job_page(response):
	result = json.loads(response)
	if result:
		jobs = result['content']['positionResult']['result']
		for job in jobs:
			company_name = job['companyFullName']
			city = job['city']
			financ = job['financeStage']
			job_name = job['positionName']
			job_year = job['workYear']
			job_createtime = job['createTime']
			job_salary = job['salary']
			job_data = {
				'company_name': company_name,
				'city': city,
				'financ': financ,
				'job_name': job_name,
				'job_year': job_year,
				'job_createtime': job_createtime,
				'job_salary': job_salary
			}
			if job_data:
				save_to_mongo(job_data)


# 保存到mongoDB数据库
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongoDB成功', result)
        return True
    return False



def main():
	for page in range(GROUP_START, GROUP_END + 1):
		time.sleep(np.random.rand() * 20)
		url = make_url(page)
		response = get_index_page(url,page)
		if response:
			parse_job_page(response)


if __name__ == '__main__':
	main()