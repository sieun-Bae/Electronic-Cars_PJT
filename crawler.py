# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

RESULT_PATH = '/Users/baesieun/baesieun/Python_Programming/Final_Project/'
now = datetime.now()
title_text = []
date_text = []
contents_text = []
contents = []

def main():
	info_main = input("="*50+"\n"+"시작하려면 Enter를 입력해주세요."+"\n"+"="*50)

	pageNum = input("최대 크롤링할 페이지 수를 입력해주세요: ")
	query = input("검색어를 입력해주세요: ")
	sort = input("뉴스 검색 방식을 입력해주세요(관련도순 = 0 최신순 = 1 오래된순 = 2): ")
	s_date = input("시작 날짜를 입력해주세요(2019.05.27): ")
	e_date = input("끝 날짜를 입력해주세요(2019.05.27): ")

	crawler(pageNum, query, sort, s_date, e_date)

def contents(news_urls):
	'''
	for url in urls:
		response = requests.get(url)
		html = response.text

		soup = BeautifulSoup(html, 'html.parser')

		content_tags = soup.select('#content')
		for content_tag in content_tags:
			print('*')
			content.append(content_tag.text)
	'''
	for i in range(len(news_urls)):
			response = requests.get(news_urls[i])
			htmls = response.text

			soup = BeautifulSoup(htmls, 'html.parser')
			c = soup.select('article_content > br').text
			contents.append(c)
		

def crawler(pageNum, query, sort, s_date, e_date):

	s_from = s_date.replace(".","")
	e_to = e_date.replace(".","")
	page = 1
	maxpage_t = (int(pageNum) - 1) * 10 + 1 #naver 뉴스 페이지 규칙 11=2페이지, 21=3페이지 ..

	while page <= maxpage_t:
		url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page) 
		
		response = requests.get(url)
		html = response.text

		soup = BeautifulSoup(html, 'html.parser')
		'''
		atags = soup.select('._sp_each_title')
		for atag in atags:
			title_text.append(atag.text)
		'''
		date_lists = soup.select('.txt_inline')
		for date_list in date_lists:
			test = date_list.text
			date_cleansing(test)
		
		news_urls = []
		
		#<ul class="type01"> 내부에 a._sp_each_title 클래스의 <a href> 태그
		area = soup.find("ul", {"class":"type01"}).find_all("a", {"class":"_sp_each_title"})
		for tag in area:
			print(tag)
			news_urls.append(tag.get('href'))
		
		contents(news_urls)
		contents_cleansing(contents)
		
		#result = { "date": date_text, "title": title_text, "contents": contents_text }
		#print(page)
		
		#df = pd.DataFrame(result)
		page += 10
		#print(contents_text)
		'''
	outputFileName = '%s-%s-%s %s시 %s분 %s초 result.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
	df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')
	'''
def date_cleansing(test):
	try: #지난 뉴스
		pattern = '\d+.(\d+).(\d+).'

		r = re.compile(pattern)
		match = r.search(test).group(0)
		date_text.append(match)

	except AttributeError:
		#최근뉴스
		pattern = '\w* (\d\w*)'

		r=re.compile(pattern)
		match=r.search(test).group(1)
		date_text.append(match)

def contents_cleansing(contents):
	first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',  str(contents)).strip()
	second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사) 
	third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip() 
	contents_text.append(third_cleansing_contents) 


if __name__=='__main__':
	main()