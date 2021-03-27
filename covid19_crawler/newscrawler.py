from encodings import gbk

#coding=utf-8
import json
import multiprocessing
import re
import time
#import requests
from urllib import request,parse
from io import BytesIO
import gzip
import pymysql


# def ungzip(data):
#     try:
#         data=gzip.decompress(data)
#     except:
#         pass
#     return data
#当前日期
time = time.strftime("%Y-%m-%d",time.localtime())

def test():
    url="https://new.qq.com/omn/20200621/20200621A06EZN00.html"
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://new.qq.com/omn/20200621/20200621A06EZN00.html'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    htmls = resp.read()
    buff = BytesIO(htmls)
    f = gzip.GzipFile(fileobj=buff)
    content = f.read().decode('utf-8','ignore')
    print(content)

#腾讯体育CBA
def txsportCBA():
    #网页头部信息
    url ='https://sports.qq.com/cba/'
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://sports.qq.com/cba/'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    htmls = resp.read()
    buff = BytesIO(htmls)
    f = gzip.GzipFile(fileobj=buff)
    content = f.read().decode('gbk')
    #print(content)

    #缩小范围（待优化）
    res1 = r'<div class="list1 list">(.*?)</div>'
    mm1 = re.findall(res1, content, re.S|re.M)
    for value in mm1:
        print(value)
    #锁定目标
    res2 = r'<a .*? href="(.*?)" .*?>(.*?)</a>'
    mm2=re.findall(res2, value, re.I|re.S|re.M)

    for url in mm2:
        #print(url)
        newsurl = url[0]
        res3 = r'/new\.qq\.com\/(?:omn|cmsn).*\/(\w+)\.html/'
        mm3 = re.match(res3, newsurl)
        print(mm3)
        # if mm3 != None :
        #     print(mm3)
            # headers = {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            #     'Referer': newsurl
            # }
            # req = request.Request(newsurl, headers=headers)
            # resp = request.urlopen(req)
            # htmls = resp.read()
            # buff = BytesIO(htmls)
            # #f = gzip.GzipFile(fileobj=buff)
            # content = buff.read().decode('utf-8')
            # print(content)
            # 获取新闻简介
            # res4 = r'<meta name="description" content="(.*?)">'
            # mm4 = re.findall(res4, content, re.I | re.S | re.M)
            # for summary in mm4:
            #     print(summary)


    #
    # #插入数据库操作
    # db = pymysql.connect('localhost','root','root','db_database18')
    # cursor = db.cursor()
    # #SQL语句
    # query = """insert into news2020 (title, newsurl, website, websiteurl, time) values (%s,%s,%s,%s,%s)"""
    # #执行
    # for url in mm2:
    #     title = url[1]
    #     newsurl = url[0]
    #     website = '腾讯体育'
    #     websiteurl = 'https://sports.qq.com/'
    #     values = (title, newsurl, website, websiteurl, time)
    #     cursor.execute(query, values)
    # #提交
    # cursor.close()
    # db.commit()
    # db.close()

#腾讯体育NBA
def txsportNBA():
    #网页头部信息
    url ='https://sports.qq.com/nba/'
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://sports.qq.com/nba/'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    htmls = resp.read()
    buff = BytesIO(htmls)
    f = gzip.GzipFile(fileobj=buff)
    content = f.read().decode('gbk')
    #print(content)

    #缩小范围（待优化）
    res1 = r'<div class="col-left" bosszone="SY_Mainnews">(.*?)</div>'
    mm1 = re.findall(res1, content, re.S|re.M)
    for value in mm1:
        print(value)
    #锁定目标
    res2 = r'<a .*? href="(.*?)" .*?>(.*?)</a>'
    mm2=re.findall(res2, value, re.I|re.S|re.M)

    for url in mm2:
        newsurl = url[0]
        title = url[1]
        #print(newsurl)
        res3 = r'https://new\.qq\.com/rain'
        mm3 = re.match(res3, newsurl)
        if mm3 != None :
            #print(newsurl)
            #获取url中的内容
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Referer': newsurl
            }
            req = request.Request(newsurl, headers=headers)
            resp = request.urlopen(req)
            htmls = resp.read()
            buff = BytesIO(htmls)
            #f = gzip.GzipFile(fileobj=buff)
            content = buff.read().decode('UTF-8')
            #print(content)

            #获取新闻简介
            res4 = r'<meta name="description" content="(.*?)">'
            mm4 = re.findall(res4, content, re.I | re.S | re.M)
            for summary in mm4:
                print(summary)

            #插入数据库操作
            db = pymysql.connect('localhost','root','root','db_database18')
            cursor = db.cursor()
            #SQL语句
            query = """insert into news2020 (title, newsurl, website, websiteurl, time, summary) values (%s,%s,%s,%s,%s,%s)"""
            # 判断是否重复
            selectquery = """SELECT * FROM news2020 WHERE title = %s"""
            cursor.execute(selectquery, title)
            results = cursor.fetchall()
            # print(results)
            if results:
                print('该条新闻已存在')
            else:
                #执行
                website = '腾讯体育'
                websiteurl = 'https://sports.qq.com/'
                values = (title, newsurl, website, websiteurl, time, summary)
                cursor.execute(query, values)
            #提交
            cursor.close()
            db.commit()
            db.close()

#新浪体育
def sinasportNBA():
    #网页头部信息
    url ='http://sports.sina.com.cn/'
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'http://sports.sina.com.cn/'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    htmls = resp.read()
    buff = BytesIO(htmls)
    #f = gzip.GzipFile(fileobj=buff)
    content = buff.read().decode('utf-8')
    #print(content)

    res1 = r'<div style="display:none!important;">(.*?)</div>'
    mm1 = re.findall(res1, content, re.S|re.M)
    for value in mm1:
        print(value)

    res2 = r'<a .*? href="(.*?)">(.*?)</a>'
    mm2=re.findall(res2, value, re.I|re.S|re.M)

    for url in mm2:
        newsurl = url[0]
        title = url[1]
        #print(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Referer': newsurl
        }
        req = request.Request(newsurl, headers=headers)
        resp = request.urlopen(req)
        htmls = resp.read()
        buff = BytesIO(htmls)
        # f = gzip.GzipFile(fileobj=buff)
        content = buff.read().decode('UTF-8')
        #print(content)

        #获取新闻简介
        res4 = r'<meta name="description" content="(.*?)" />'
        mm4 = re.findall(res4, content, re.I | re.S | re.M)
        for summary in mm4:
            print(summary)

        # 插入数据库操作
        db = pymysql.connect('localhost', 'root', 'root', 'db_database18')
        cursor = db.cursor()
        # SQL语句
        query = """insert into news2020 (title, newsurl, website, websiteurl, time, summary) values (%s,%s,%s,%s,%s,%s)"""

        #判断是否重复
        selectquery = """SELECT * FROM news2020 WHERE title = %s"""
        cursor.execute(selectquery, title)
        results = cursor.fetchall()
        #print(results)
        if results :
            print('该条新闻已存在')
        else:
            # 执行插入
            website = '新浪体育'
            websiteurl = 'http://sports.sina.com.cn/'
            values = (title, newsurl, website, websiteurl, time, summary)
            cursor.execute(query, values)
        # 提交
        cursor.close()
        db.commit()
        db.close()

#搜狐体育
def souhusport():
    #网页头部信息
    url ='https://sports.sohu.com/s/nba?spm=smpc.fb-sports-home.top-subnav.15.1592458689454IkZ1v9o'
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://sports.sohu.com/s/nba?spm=smpc.fb-sports-home.top-subnav.15.1592458689454IkZ1v9o'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    htmls = resp.read()
    buff = BytesIO(htmls)
    #f = gzip.GzipFile(fileobj=buff)
    content = buff.read().decode('utf-8')
    #print(content)

    res1 = r'<ul class="news-list first" data-spm="top-news-1">(.*?)</ul>'
    mm1 = re.findall(res1, content, re.S|re.M)
    for value in mm1:
        print(value)

    res2 = r'<a href="//(.*?)" .*?>(.*?)</a>'
    mm2=re.findall(res2, value, re.I|re.S|re.M)

    for url in mm2:
        newsurl1 = url[0]
        title = url[1]
        newsurl = 'https://'+newsurl1
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Referer': newsurl
        }
        req = request.Request(newsurl, headers=headers)
        resp = request.urlopen(req)
        htmls = resp.read()
        buff = BytesIO(htmls)
        # f = gzip.GzipFile(fileobj=buff)
        content = buff.read().decode('UTF-8')

        #获取新闻简介
        res4 = r'<meta name="description" content="(.*?)" />'
        mm4 = re.findall(res4, content, re.I | re.S | re.M)
        for summary in mm4:
            print(summary)

        # 插入数据库操作
        db = pymysql.connect('localhost', 'root', 'root', 'db_database18')
        cursor = db.cursor()
        # SQL语句
        query = """insert into news2020 (title, newsurl, website, websiteurl, time, summary) values (%s,%s,%s,%s,%s,%s)"""

        #判断是否重复
        selectquery = """SELECT * FROM news2020 WHERE title = %s"""
        cursor.execute(selectquery, title)
        results = cursor.fetchall()
        #print(results)
        if results :
            print('该条新闻已存在')
        else:
            # 执行插入
            website = '搜狐体育'
            websiteurl = 'https://sports.sohu.com/'
            values = (title, newsurl, website, websiteurl, time, summary)
            cursor.execute(query, values)
        # 提交
        cursor.close()
        db.commit()
        db.close()



if __name__ == '__main__':
    #test()
    #txsportCBA()
    txsportNBA()
    sinasportNBA()
    souhusport()