import requests
import json
import datetime
import re
import sys
import os
from urllib.parse import urlencode
from contextlib import closing
from requests.packages import urllib3
import random
urllib3.disable_warnings()
hds = ['Mozilla/5.0 (Linux; Android 4.4.4; CHM-CL00 Build/CHM-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 V1_AND_SQ_6.3.7_374_YYB_D QQ/6.3.7.2795 NetType/WIFI WebP/0.3.2 Pixel/720',		'Mozilla/5.0 (Linux; Android 5.0.1; HUAWEI GRA-TL00 Build/HUAWEIGRA-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.2 TBS/036215 Safari/537.36 MicroMessenger/6.3.16.49_r03ae324.780 NetType/WIFI Language/zh_CN',
		'Mozilla/5.0 (Linux; Android 5.0.1; HUAWEI GRA-CL00 Build/HUAWEIGRA-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.2 TBS/036519 Safari/537.36 V1_AND_SQ_6.3.1_350_YYB_D QQ/6.3.1.2735 NetType/WIFI WebP/0.3.0 Pixel/1080',
	   'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13D15 QQ/6.3.3.432 V1_IPH_SQ_6.3.3_1_APP_A Pixel/1080 Core/UIWebView NetType/WIFI Mem/104',
	   'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13C75 QQ/6.2.3.409 Pixel/750 NetType/WIFI Mem/703',
	   'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; Coolpad 8297-T01 Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025477 Mobile Safari/533.1 V1_AND_SQ_5.9.0_270_YYB_D QQ/5.9.0.2530 NetType/WIFI WebP/0.3.0 Pixel/720',
		'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'
	   ]
headers = {
            'user-agent':random.choice(hds),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0'
}
# 报错提示模块
def errors_print():
    print(u"在文件中输入分享出来的链接，可以输入多个，用逗号隔开，可以换行\n")

# 解析分享的文件
def parse_share_url(filename):
	with open(filename,'r') as f:
		url = f.read().rstrip().lstrip()
		url = url.replace("\t", ",").replace("\r", ",").replace("\n", ",").replace(" ", ",")
		url = url.split(",")
		print(url)
		urls = list()
	for url_site in url:
		site = url_site.lstrip().rstrip()
		if site:
			urls.append(site)
	return urls

# 解析文件里面读取出来的链接
def parse_url(urls):
	musics_id = []
	challenges_id = []
	users_id = []
	for i in range(len(urls)):
		url = urls[i]
		if url:
			# 分析链接是音乐链接
			if re.search('share/music',url):
				music_id = re.findall('share/music/(.*)\?', url)
				# if len(musics_id):
				musics_id.append(music_id[0])
				for music in musics_id:
					print(music)
					if music not in os.listdir():
						os.mkdir(music)
					download_music_media(music)


			# 分析链接是主题链接
			if re.search('share/challenge', url):
				challenge_id = re.findall('share/challenge/(.*)\?',url)
				challenges_id.append(challenge_id[0])
				for challenge in challenges_id:

					if challenge not in os.listdir():
						os.mkdir(challenge)
					# print(challenge)
					download_challenge_media(challenge)

			# 分析链接是用户主页,请求下载的是用户喜欢的视频
			if re.search('share/user', url):
				user_id = re.findall('share/user/(.*)/\?',url)
				users_id.append(user_id[0])
				for u_id in users_id:
					if u_id not in os.listdir():
						os.mkdir(u_id)
					# print(challenge)
					download_ulike_media(u_id)
# 获取音乐下的视频信息
def download_music_media(music):
	params = {
		'music_id': music,
		'cursor': '0',
		'count': '20',
		'type': '6',
		'device_id': '51908931552',
		'aid': '1128'
	}

	# 拼接视频信息
	def get_musicmedia_url(cursor=None,video_count=0):
		video_names = []
		video_urls = []
		if cursor:
			params['cursor'] = str(cursor)
		music_url = 'https://api.amemv.com/aweme/v1/music/aweme/?' + urlencode(params)
		response = requests.get(music_url, headers=headers, verify=False)
		music_ms = json.loads(response.text)
		for aweme_url in music_ms['aweme_list']:
			video_count += 1
			# share_desc = aweme_url['desc']
			share_descs = aweme_url['share_url']
			share_desc = re.findall('/share/video/(.*)/\?',share_descs)[0]
			video_names.append(str(share_desc)+ '.mp4')
			video_urls.append(aweme_url['share_info']['share_url'])
		parse_media_url(video_names, video_urls,music)
		if music_ms.get('has_more') == 1:
			return get_musicmedia_url(music_ms.get('cursor'), video_count)

	video_count = get_musicmedia_url()
	if video_count == 0:
		print('这个音乐下没有视频')

# 解析视频链接获得真实的下载地址
def parse_media_url(video_names, video_urls,music):
	for item in range(len(video_names)):
		# temp = video_names[item].replace('\\', '')
		# video_name = temp.replace('/', '')
		_download_video(video_urls[item], os.path.join(music,video_names[item]))

# 下载模块
def _download_video(video_url, path):
	video_content = get_video_url(video_url)
	# print(video_content)
	rec = re.compile(r'class="video-player" src="(.*?)"')
	pattern = re.compile(r'playwm')
	downloadwm_url = rec.search(video_content).group(1)
	# 构建无水印下载链接
	download_url = re.sub(pattern, 'play', downloadwm_url)
	print('正在下载：',download_url, path)
	with closing(requests.get(download_url, headers=headers, stream=True, verify=False)) as response:
		chunk_size = 1024
		if response.status_code == 200:
			with open(path, 'wb') as f:
				for data in response.iter_content(chunk_size=chunk_size):
					f.write(data)
				# flush() 方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，同时清空缓冲区，不需要是被动的等待输出缓冲区写入。
					f.flush()

# 请求真实的视频下载接口
def get_video_url(video_url):
	try:
		response = requests.get(url=video_url, headers=headers, verify=False)
		if response.status_code == 200:
			return response.text
	except RequestException:
		print('请求视频接口错误', url)
		return None

# 下载主题下的视频
def download_challenge_media(challenge):
	# print(challenge)
	params = {
		'ch_id': challenge,
		'cursor': '0',
		'count': '20',
		'type': '5',
		'device_id': '51908931552',
		'aid': '1128'
	}

	# 拼接视频信息
	def get_challengemedia_url(cursor=None, video_count=0):
		video_names = []
		video_urls = []
		if cursor:
			params['cursor'] = str(cursor)
		challenge_url = 'https://api.amemv.com/aweme/v1/challenge/aweme/?' + urlencode(params)
		response = requests.get(challenge_url, headers=headers, verify=False)
		challenge_ms = json.loads(response.text)
		for aweme_url in challenge_ms['aweme_list']:
			video_count += 1
			share_descs = aweme_url['share_url']
			share_desc = re.findall('/share/video/(.*)/\?', share_descs)[0]
			video_names.append(str(share_desc) + '.mp4')
			video_urls.append(aweme_url['share_info']['share_url'])
		parse_media_url(video_names, video_urls, challenge)
		if challenge_ms.get('has_more') == 1:
			return get_challengemedia_url(challenge_ms.get('cursor'), video_count)
	video_count = get_challengemedia_url()
	if video_count == 0:
		print('这个主题下没有视频')

# 解析获得点赞的视频下载链接
def download_ulike_media(u_id):
	p = os.popen('node fuck-byted-acrawler.js %s' % u_id)
	signature = p.readlines()[0]
	params = {
		'user_id': str(u_id),
		'count': '21',
		'max_cursor': '0',
		'aid': '1128',
		'_signature': signature
	}
	# 拼接视频信息
	def get_ulike_url(max_cursor=None, video_count=0):
		video_names = []
		video_urls = []
		url = 'https://www.amemv.com/share/video/'
		if max_cursor:
			params['max_cursor'] = str(max_cursor)
		ulike_url = 'https://www.douyin.com/aweme/v1/aweme/favorite/?' + urlencode(params)
		# print(ulike_url)
		res = requests.get(ulike_url, headers=headers, verify=False)
		ulike_ms = json.loads(res.content.decode('utf-8'))
		favorite_list = str(ulike_ms['aweme_list'])
		v_id = re.findall('https://www.amemv.com/share/video/(.*?)\'',favorite_list)
		for l in v_id:
			share_desc = l + '.mp4'
			s_url = url + l
			video_names.append(share_desc)
			video_urls.append(s_url)
		parse_media_url(video_names, video_urls, u_id)
		if ulike_ms.get('has_more') == 1:
			return get_ulike_url(ulike_ms.get('max_cursor'), video_count)
	video_count = get_ulike_url()
	if video_count == 0:
		print('这个用户没有喜欢的视频')



if __name__ == '__main__':
	urls = None
	if len(sys.argv) < 2:
		filename = "share-url.txt"
		if os.path.exists(filename):
			urls = parse_share_url(filename)
		else:
			errors_print()
			sys.exit(1)
	else:
		urls = sys.argv[1].split(",")

	if len(urls) == 0 or urls[0] == "":
		errors_print()
		sys.exit(1)
	parse_url(urls)