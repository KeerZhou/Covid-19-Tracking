# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 15:35:25 2021

@author: sjy
"""

from encodings import gbk

#coding=utf-8
import json
import re
import time
#import requests
from urllib import request,parse
from urllib.request import ProxyHandler,build_opener
from io import BytesIO
import pymysql
import gzip

#当前日期
time = time.strftime("%Y-%m-%d",time.localtime())

db = pymysql.connect('localhost','root','root','covid19_data')
cursor = db.cursor()

#proxy = '127.0.0.1:11000'
#proxy_handler = ProxyHandler({
#    'http' : 'http://' + proxy,
#    'https' : 'https://' + proxy
#})
#opener = build_opener(proxy_handler)
#SQL语句
query = "insert into covid19_table_news (news_title, news_url, news_content, source, source_url, publish_date) values (%s,%s,%s,%s,%s,%s)"
selectquery = "SELECT * FROM covid19_table_news WHERE news_title = %s"

def dingxiang_news():
    # 丁香园
    for page in range(1,6):
        #https://www.medrxiv.org/search/COVID-19%20numresults%3A75%20sort%3Arelevance-rank
        url="https://search.dxy.cn/?words=%E6%96%B0%E5%86%A0&page="+ str(page) +"&age=30&limit=15"
        headers ={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Referer':'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json'
        }
        #resp = opener.open(url)
        req = request.Request(url,headers=headers)
        resp = request.urlopen(req)
        original_htmls = resp.read()
        #print(htmls)
        html = str(original_htmls, encoding='utf-8')
        #print(html)
        
        res1 = '<div class="main-item j-main-it".*?>.*?<a href=".*?" target="_blank">(.*?)</a>'
        res2 = '<div class="main-item j-main-it".*?>.*?<a href="(.*?)" target="_blank">.*?</a>'
        res3 = '<span class="it-split">-</span>.*?<span class="it-split">-</span>(.*?)</p>'
        res4 = '<p class="it-cnt">.*?<a target="_blank">(.*?)</a>'
        mm1 = re.findall(res1, html, re.S|re.M)
        mm2 = re.findall(res2, html, re.S|re.M)
        mm3 = re.findall(res3, html, re.S|re.M)
        mm4 = re.findall(res4, html, re.S|re.M)
#        print(len(mm4))
#        for value in mm4:
#            print(value)
        for i in range(0,len(mm1)):
            a = mm1[i].replace('<em class="red">','')
            news_title = a.replace('</em>','')
            news_url = mm2[i]
            publish_date = mm3[i].strip()[:10]
            c = mm4[i].replace('<em class="red">','')
            content = c.replace('</em>','')
#            print(news_title)
#            print(news_url)
#            print(publish_date)
#            print(content)
            
            #判断是否重复
            query_values = (news_title)
            cursor.execute(selectquery, query_values)
            results = cursor.fetchall()
            #print(results)
            if results :
                print('该条已存在')
            else:
                values = (news_title,news_url,content,'丁香园'
                          , 'https://portal.dxy.cn/', publish_date)
                print(values)
                cursor.execute(query, values)
    # 提交
    cursor.close()
    db.commit()
    db.close()
    
    
def CCTV_news():
    #CCTV
    #https://search.cctv.com/search.php?qtext=%E6%96%B0%E5%86%A0&type=web
    for page in range(1,6):
        url="https://search.cctv.com/search.php?qtext=%E6%96%B0%E5%86%A0&sort=relevance&type=web&vtime=&datepid=1&channel=&page=" + str(page)
        headers ={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Referer':'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json'
                }
        #resp = opener.open(url)
        req = request.Request(url,headers=headers)
        resp = request.urlopen(req)
        original_htmls = resp.read()
        #print(htmls)
        html = str(original_htmls, encoding='utf-8')
        #print(html)
        
        res1 = '<a  id="web_content_.*?" href="link.*?" target="_blank">(.*?)</a>'
        res2 = '<a  id="web_content_.*?" href="link(.*?)" target="_blank">.*?</a>'
        res3 = '<span class="tim".*?>(.*?)</span>'
        res4 = '<p class="bre">(.*?)</p>'
        mm1 = re.findall(res1, str(html), re.S|re.M)
        mm2 = re.findall(res2, str(html), re.S|re.M)
        mm3 = re.findall(res3, str(html), re.S|re.M)
        mm4 = re.findall(res4, str(html), re.S|re.M)
#        print(len(mm1))
#        print(len(mm2))
#        print(len(mm3))
#        print(len(mm4))
#        for i in range(0,len(mm1)):
#            print(mm1[i])
#            print(mm2[i])
#            print(mm3[i])
#            print(mm4[i][227:])
            
        for i in range(0,len(mm1)):
            a = mm1[i].replace('<font color="red">','')
            news_title = a.replace('</font>','')
            res5 = '(.*?)&p'
            mm5 = re.findall(res5, str(mm2[i][18:91]), re.S|re.M)
            news_url = mm5[0]
            publish_date = mm3[i][5:16]
            c = mm4[i][295:].replace('<font color="red">','')
            content = c.replace('</font>','')
#            print(news_title)
#            print(news_url)
#            print(publish_date)
#            print(content)
        
            #判断是否重复
            query_values = (news_title)
            cursor.execute(selectquery, query_values)
            results = cursor.fetchall()
            #print(results)
            if results :
                print('该条已存在')
            else:
                values = (news_title,news_url,content,'央视网'
                          , 'https://www.cctv.com/', publish_date)
                print(values)
                cursor.execute(query, values)
    # 提交
    cursor.close()
    db.commit()
    db.close()


if __name__ == '__main__':
    #dingxiang_news()
    CCTV_news()

