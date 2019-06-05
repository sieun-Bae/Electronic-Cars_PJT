import re
import json
import math
import datetime
import requests
import urllib.request
import urllib.error
import urllib.parse
from bs4 import BeautifulSoup

naver_client_id = "tUeiLShUyPmjHrqJvZd3"
naver_client_secret = "ceIN9Ru18M"

def get_blog_count(query, display):
	encode_query = urllib.parse.quote(query)
	search_url = "http://openapi.naver.com/v1/search/blog?query="+encode_query
	request = urllib.request.Request(search_url)

	request.add_header("X-Naver-Client-Id", naver_client_id)
	request.add_header("X-Naver-Client-Secret", naver_client_secret)

	response = urllib.request.urlopen(request)
	response_code = response.getcode()
	print(response_code)
	if response_code is 200:
		response_body = response.read()
		response_body_dict = json.loads(response_body.decode('utf-8'))

		if response_body_dict['total']==0:
			blog_count = 0
		else:
			blog_total = math.ceil(response_body_dict['total']/int(display))

			if blog_total >= 1000:
				blog_count = 50
			else:
				blog_count = 50

	return blog_count
def get_blog_post(query, display, start_index, sort):
	global no, fs

	encode_query = urllib.parse.quote(query)
	search_url = "http://openapi.naver.com/v1/search/blog?query="+encode_query+"&display="+str(display)+'&start='+str(start_index)+"&sort="+sort

	request = urllib.request.Request(search_url)

	request.add_header("X-Naver-Client-Id", naver_client_id)
	request.add_header("X-Naver-Client-Secret", naver_client_secret)

	response = urllib.request.urlopen(request)
	response_code = response.getcode()

	if response_code is 200:
		response_body = response.read()
		response_body_dict = json.loads(response_body.decode('utf-8'))
		for item_index in range(0, len(response_body_dict['items'])):
			try:
				remove_html_tag = re.compile('<.*?>')
				title = re.sub(remove_html_tag, '', response_body_dict['items'][item_index]['title'])
				link = response_body_dict['items'][item_index]['link'].replace("amp;","")
				description = re.sub(remove_html_tag, '', response_body_dict['items'][item_index]['description'])
				blogger_name = response_body_dict['items'][item_index]['bloggername']
				blogger_link = response_body_dict['items'][item_index]['bloggerlink']
				post_date = response_body_dict['items'][item_index]['postdate']

				no += 1
				post_code = requests.get(link)
				post_text = post_code.post_text
				post_soup = BeautifulSoup(post_text, 'lxml')

				for mainFrame in post_soup.select('iframe#mainFrame'):
					blog_post_url = "http://blog.naver.com"+mainFrame.get('src')
					blog_post_code = requests.get(blog_post_url)
					blog_post_text = blog_post_code.post_text
					blog_post_soup = BeautifulSoup(post_text, 'lxml')

					for blog_post_content in blog_post_soup.select('div#postViewArea'):
						blog_post_content_text = blog_post_content.get_text()
						blog_post_full_contents = str(blog_post_content_text)
						blog_post_full_contents = blog_post_full_contents.replace("\n\n", "\n")
						fs.write(blog_post_full_contents+"\n")
			except:
				item_index += 1


if __name__ == '__main__':
	no = 0
	query = '전기차 활성화'
	display = 10
	start = 1
	sort = "sim"

	fs = open(query + ".txt", "a", encoding="utf-8")
	blog_count = get_blog_count(query, display)
	for start_index in range(start, blog_count + 1, display):
		get_blog_post(query, display, start_index, sort)
	fs.close()

