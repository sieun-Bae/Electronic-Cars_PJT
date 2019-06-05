from itertools import count
from collections import OrderedDict

from bs4 import BeautifulSoup
import requests
import urllib.request as req

def get_url():
	url = "https://search.naver.com/search.naver"
	hrd = {'User-Agent' : 'Mozilla/5.0', 'referer' : 'http://naver.com'}

	post_dict = OrderedDict()
	cnt = 1

	query = input("검색어를 입력해주세요: ")
	page = int(input("크롤링할 페이지를 입력해주세요: "))

	for page in count(1,1):
		param = {
			'where' :'post',
			'query' : query,
			'start' : (page - 1) * 10 + 1
		}

		response = requests.get(url, params = param, headers = hrd)
		soup = BeautifulSoup(response.text, 'html.parser')
		
		area = soup.find("div", {"class":"blog section _blogBase _prs_blg"}).find_all("a", {"class":"url"})

		for tag in area:
			url1 = tag.get('href')

			post_dict[tag['href']] = tag.text
			cnt += 1

	return url1


def get_final_url(url):
	try:
		url_1 = url
		html_result = requests.get(url_1)
		soup_temp = BeautifulSoup(html_result.text, 'html.parser')
		area_temp = soup_temp.find(id='screenFrame')
		url_2 = area_temp.get('src')
	except:
		try:
			area_temp = soup_temp.find(id='mainFrame')
			url_3 = area_temp.get('src')
			url_4 = "http://blog.naver.com"+url_3
		except:
			return None
	try:
		html_result = requests.get(url_2)
		soup_temp = BeautifulSoup(html_result.text, 'html.parser')
		area_temp = soup_temp.find(id='mainFrame')
		url_3 = area_temp.get('src')
		url_4 = "http://blog.naver.com"+url_3
	except:
		print("error")
		return None

	return url_4

def final_url():
	url1 = get_url()

	f_url = ''
	for i in range(len(url1)):
		f_url = f_url + '\n' + get_final_url(url1[i])

	return f_url
	
if __name__ == '__main__':
	main()