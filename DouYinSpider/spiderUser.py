import requests
import json
import datetime
import re
import sys
import os
from contextlib import closing
from requests.packages import urllib3
urllib3.disable_warnings()
headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0'
}

# 根据抓包的文件获得入口，分析请求入口的信息，得到虚假的视频入口和视频名称
def parse_app_package(user_id):
    video_names = []
    video_urls = []
    # 通过抓包获取的入口链接
    url = 'https://api.amemv.com/aweme/v1/discover/search/?cursor=0&keyword=%s&count=10&type=1&ts=1528115402&app_type=lite&os_api=22&device_type=M623C&device_platform=android&ssmix=a&iid=31808367986&manifest_version_code=179&dpi=320&uuid=869716027150235&version_code=179&app_name=aweme&version_name=1.7.9&openudid=ffa30e1978cec5ed&device_id=51908931552&resolution=720*1280&os_version=5.1.1&language=zh&device_brand=CMDC&ac=wifi&update_version_code=1790&aid=1128&channel=sem_baidu_dy_pz&_rticket=1528115402836&as=a115f321aaecdbc0056554&cp=39c6bf52a45a1307e1mfsy&mas=00c96bfd6f0b31a1dc9abf12f3aca20de42cacac6cac0c0cc64626' % user_id
    # verify=False用于忽略https请求报错
    response = requests.get(url, headers=headers, verify=False)
    user_ms = json.loads(response.text)
    # print(user_ms)
    # 这个链接和我们输入的抖音号不同
    u_id = user_ms['user_list'][0]['user_info']['uid']
    works_num = user_ms['user_list'][0]['user_info']['aweme_count']
    user_name = user_ms['user_list'][0]['user_info']['nickname']
    # 带字符的名字的和这个id和uid的值不同，之后请求带入的uid都是这里获取到的unique_id
    unique_id = user_ms['user_list'][0]['user_info']['unique_id']
    # print(user_id,works_num,user_name)
    # 到这一步在APP中对应的操作是我们手动搜索抖音号后点击进入到这个用户的主页
    user_url = 'https://www.amemv.com/aweme/v1/aweme/post/?user_id={}&max_cursor=0&count={}'.format(u_id, works_num)
    user_response = requests.get(user_url, headers=headers, verify=False)
    userpage_ms = json.loads(user_response.text)
    # 根据抓包的结果，这里获取到这个用户的发布的全部作品数量
    for aweme_url in userpage_ms['aweme_list']:
        share_desc = aweme_url['desc']
        if share_desc == None:
            nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            video_names.append(str(nowTime) + '.mp4')
        else:
            video_names.append(str(share_desc) + '.mp4')
        video_urls.append(aweme_url['share_info']['share_url'])
    return video_names, video_urls, user_name


# 根据上述的虚假接口请求，解析获得真实接口并下载
def download_video(video_names,video_urls,user_name):
    for item in range(len(video_names)):
        _download_video(video_urls[item],os.path.join(user_name, video_names[item]))

def _download_video(video_url,path):

    video_content = get_video_url(video_url)
    rec = re.compile(r'class="video-player" src="(.*?)"')
    pattern = re.compile(r'playwm')
    downloadwm_url = rec.search(video_content).group(1)
    download_url = re.sub(pattern, 'play', downloadwm_url)
    print(download_url, path)
    with closing(requests.get(download_url, headers=headers, stream=True, verify=False)) as response:
        chunk_size = 1024
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for data in response.iter_content(chunk_size=chunk_size):
                    f.write(data)
                # flush() 方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，同时清空缓冲区，不需要是被动的等待输出缓冲区写入。
                    f.flush()

# 请求虚假接口
def get_video_url(video_url):
	try:
		response = requests.get(url=video_url, headers=headers, verify=False)
		if response.status_code == 200:
			return response.text
	except RequestException:
		print('请求视频接口错误', url)
		return None



def main():
    user_id = input('请输入要下载作品的抖音号：')
    # 解析入口，获得视频名称，和虚假入口
    video_names,video_urls,user_name = parse_app_package(user_id)
    if user_name not in os.listdir():
        os.mkdir(user_name)
    # 解析虚假入口获得真实视频地址
    download_video(video_names, video_urls, user_name)

if __name__ == '__main__':
    main()
