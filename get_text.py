from itertools import count
from collections import OrderedDict

from bs4 import BeautifulSoup
import requests
import urllib.request as req

def get_text(final_url):
	try:
		res = req.urlopen(final_url)
		soup = BeautifulSoup(res, 'html.parser')
		temp = soup.select("#se_textarea")

		title = soup.findAll("span", {"class":"pcol1 itemSubjectBoldfont"})
		for a in title:
			text = a.get_text()

		temp = soup.findAll("div", {"id":"postViewArea"})
		for a in temp:
			text = a.get_text()

	except:
		print("크롤링 실패")