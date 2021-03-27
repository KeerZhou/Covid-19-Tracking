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

#当前日期
time = time.strftime("%Y-%m-%d",time.localtime())

db = pymysql.connect('localhost','root','root','covid19_data')
cursor = db.cursor()

proxy = '127.0.0.1:11000'
proxy_handler = ProxyHandler({
    'http' : 'http://' + proxy,
    'https' : 'https://' + proxy
})
opener = build_opener(proxy_handler)

def medrxiv_acticle():
    # medrxiv文章
    #https://www.medrxiv.org/search/COVID-19%20numresults%3A75%20sort%3Arelevance-rank
    url="https://www.medrxiv.org/search/COVID-19%20numresults%3A75%20sort%3Arelevance-rank"
#    headers ={
#        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
#        'Referer':'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json'
#    }
    resp = opener.open(url)
    htmls = resp.read()
    #print(htmls)
    #medrxiv_data = json.loads(htmls)
    res1 = '<span class="highwire-cite-title">(.*?)</span>'
    res2 = '<span class="doi_label">doi:</span>(.*?)</span>'
    res3 = '<span class="highwire-citation-author first".*?><span class="nlm-given-names">(.*?)</span>'
    res4 = '<span class="highwire-citation-author first".*?>.*?<span class="nlm-surname">(.*?)</span></span>'
    mm1 = re.findall(res1, str(htmls), re.S|re.M)
    mm2 = re.findall(res2, str(htmls), re.S|re.M)
    mm3 = re.findall(res3, str(htmls), re.S|re.M)
    mm4 = re.findall(res4, str(htmls), re.S|re.M)
    
#    print(len(mm1))
#    print(len(mm3))
#    for i in range(0,len(mm1)):
#        print(mm1[i])
#        print(mm2[i])
#        print(mm2[i][25:35].replace('.','-'))
#        print(mm3[i]+' '+mm4[i])


    
#    title = []
#    url = []
#    publish_date = []
#    author = []
#    content = []
    #SQL语句
    query = "insert into covid19_table_article (title, author, content, publish_date, source, source_url, url) values (%s,%s,%s,%s,%s,%s,%s)"
    selectquery = "SELECT * FROM covid19_table_article WHERE title = %s"
        
    for i in range(0,len(mm1)):
    #for i in range(0,5):
        abstract_url = mm2[i]
        abstract_resp = opener.open(abstract_url)
        abstract_htmls = abstract_resp.read()
        #print(htmls)
        res5 = '</h2><p id=".*?">(.*?)</p>'
        mm5 = re.findall(res5, str(abstract_htmls.decode('utf-8')), re.S|re.M)
        #print(mm1[i])
        #print(mm2[i])
        #print(mm2[i][25:35].replace('.','-'))
        #print(mm3[i]+' '+mm4[i])
        #print(mm5)
        
        #判断是否重复
        query_values = (mm1[i])
        cursor.execute(selectquery, query_values)
        results = cursor.fetchall()
        #print(results)
        if results :
            print('该条已存在')
        else:
            values = (mm1[i], mm3[i]+' '+mm4[i], mm5[0]
            , mm2[i][25:35].replace('.','-'), 'medRxiv', 'https://www.medrxiv.org/',mm2[i])
            print(values)
            cursor.execute(query, values)
    # 提交
    cursor.close()
    db.commit()
    db.close()
    

if __name__ == '__main__':
    medrxiv_acticle()
    
    
    
    
    