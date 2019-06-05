from itertools import count
from collections import OrderedDict

from bs4 import BeautifulSoup
import requests
import urllib.request as req

#from final_url import *
#from get_text import *

RESULT_PATH = '/Users/baesieun/baesieun/Python_Programming/Final-Project_SRC/'

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


def main():
	query = input("query?")
	pageNum = input("page?")
	maxpage_t = (int(pageNum) - 1)*10+1

	page=1
	url1 = '' #completely raw url
	f_url = '' #final url

	while page <= maxpage_t:
		url = "https://search.naver.com/search.naver?&where=post&query="+query+"&start="+str(page)
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		
		area = soup.find("div", {"class":"blog section _blogBase _prs_blg"}).find_all("a", {"class":"url"})

		for tag in area:
			if "daum" in tag['href'] or tistory in tag['href']:
				continue
			url1 = tag.get('href')
			url2 = get_final_url(url1)	
			f_url = f_url + '\n' + url2
		page+=10
	print(f_url)
	'''
	for i in range(len(url1)):
		temp = get_final_url(url1[i])
		url2 = url2 + '' + temp
	print(url1)
	print(url2)
	'''
if __name__ == '__main__':
	main()

#print(get_url())
