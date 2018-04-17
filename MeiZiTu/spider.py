import requests
from multiprocessing import Pool
from requests.exceptions import RequestException
import json
import sys
from bs4 import BeautifulSoup
import os
from hashlib import md5
import pymongo
from config import *
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}

# 构建每一页的链接
def get_index_page(page_number):

    url = 'http://www.meizitu.com/a/more_{}.html' .format(page_number)
    try:
        reponse = requests.get(url, headers=headers)
        reponse.encoding = reponse.apparent_encoding
        if reponse.status_code == 200:
            return reponse.text
        return None
    except RequestException:
        print('请求列表页错误')
        return None

# 请求图集详情页
def get_detail_page(url):
    try:
        reponse = requests.get(url, headers=headers)
        reponse.encoding = reponse.apparent_encoding
        if reponse.status_code == 200:
            # print(reponse.text)
            return reponse.text
        return None
    except RequestException:
        print('请求详情页错误', url)
        return None



# 解析列表页，把每一页中的单个图集链接解析出来
def parse_index_page(html):
    url = []
    soup = BeautifulSoup(html, 'lxml')
    url_list = soup.select('#maincontent > div.inWrap > ul > li > div > h3 > a')
    length = len(url_list)
    for i in range(length):
        url = url + [url_list[i].attrs["href"]]
    return url

# 解析图集详情页
def parse_detail_page(html, url):
    img_list = []
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    img = soup.select('#picture > p > img')

    # print(title, img)
    length = len(img)
    for i in range(length):
        img_list = img_list + [img[i].attrs["src"]]
    for img_path in img_list:
        download_image(img_path)
    return {
        'title': title,
        'url': url,
        'img_path': img_list
    }


# 下载图片
def download_image(url):
    print('正在下载', url)
    try:
        reponse = requests.get(url, headers=headers)
        if reponse.status_code == 200:
            # print(reponse.text)
            save_image(reponse.content)
        return None
    except RequestException:
        print('请求下载图片错误', url)
        return None

# 保存图片，校验去重
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


# 保存到mongoDB数据库
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongoDB成功', result)
        return True
    return False



def main(page_number):
    html = get_index_page(page_number)
    for url in parse_index_page(html):
        html = get_detail_page(url)
        # print(html)
        if html:
            result = parse_detail_page(html, url)
            if result:
                save_to_mongo(result)


if __name__ == '__main__':
    for groups in range(GROUP_START, GROUP_END + 1):
        main(groups)
    # groups = [x for x in range(GROUP_START, GROUP_END + 1)]
    # pool = Pool()
    # pool.map(main, groups)8