# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re

title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
result={}

#store in local
RESULT_PATH = '/Users/baesieun/baesieun/Python_Programming/Final-Project_SRC/'
now = datetime.now() 

#preprocessing date
def date_cleansing(test):
    try:
        pattern = '\d+.(\d+).(\d+).'  

        r = re.compile(pattern)
        match = r.search(test).group(0)  
        date_text.append(match)
        
    except AttributeError:
        pattern = '\w* (\d\w*)'     
        
        r = re.compile(pattern)
        match = r.search(test).group(1)
        date_text.append(match)


#preprocessing contents
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '', 
                                      str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', 
                                       first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    

def crawler(maxpage,query,sort,s_date,e_date):

    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    page = 1  
    maxpage_t =(int(maxpage)-1)*10+1   # rule: 11= 2p 21=3p 31=4p

    while page <= maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        
        response = requests.get(url)
        html = response.text
 
        soup = BeautifulSoup(html, 'html.parser')
 
        #abstract title and link from <a> tag
        atags = soup.select('._sp_each_title')
        for atag in atags:
            title_text.append(atag.text)     #title
            link_text.append(atag['href'])   #link
            
        #abstract source
        source_lists = soup.select('._sp_each_source')
        for source_list in source_lists:
            source_text.append(source_list.text)   

        #abstract date 
        date_lists = soup.select('.txt_inline')
        for date_list in date_lists:
            test=date_list.text   
            date_cleansing(test)  

        #abstract contents
        contents_lists = soup.select('ul.type01 dl')
        for contents_list in contents_lists:
            contents_cleansing(contents_list) 
        
        #store list -> dict
        result= {"date" : date_text , "title":title_text ,  "source" : source_text ,"contents": contents_text ,"link":link_text }  
        print(page)
        
        df = pd.DataFrame(result)
        page += 10
    
    
    # set file name
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')
    
    

def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    
    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")  
    query = input("검색어 입력: ")  
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")    #관련도순=0  최신순=1  오래된순=2
    s_date = input("시작날짜 입력(2019.01.04):")  #2019.01.04
    e_date = input("끝날짜 입력(2019.01.05):")   #2019.01.05
    
    crawler(maxpage,query,sort,s_date,e_date) 
    
main()
