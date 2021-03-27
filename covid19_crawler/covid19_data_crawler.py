# https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports_us/04-17-2020.csv
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
import datetime

db = pymysql.connect('localhost','root','root','covid19_data')
cursor = db.cursor()

proxy = '127.0.0.1:11000'
proxy_handler = ProxyHandler({
    'http' : 'http://' + proxy,
    'https' : 'https://' + proxy
})
opener = build_opener(proxy_handler)

# 全球疫情数据
def WorldwideData():
    #url="https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/1/query?f=json&where=Country_Region%3D%27US%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc%2CCountry_Region%20asc%2CProvince_State%20asc&resultOffset=0&resultRecordCount=200&resultType=standard&cacheHint=true"
    #https://coronavirus.jhu.edu/map.html
    #https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json
    # 全世界各国数据
    url="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json"
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.json'
    }
    resp = opener.open(url)
    htmls = resp.read()
    #print(htmls)
    covid19_data = json.loads(htmls)
    #print(covid19_data)
#    req = request.Request(url,headers=headers)
#    resp = request.urlopen(req)
#    #print(resp)
#    htmls = resp.read()
#    print(htmls)
#    covid19_data = json.loads(htmls)
#    #print(covid19_data)
    res1 = r'}, \'(.*?)\': {'
    mm1 = re.findall(res1, str(covid19_data), re.S|re.M)
    #国家简称
    country_abbr_list = ['AFG']
    for value in mm1:
        #print(value)
        country_abbr_list.append(value)
    #print(country_abbr_list)
    #国家全称
    country_list = []
    confirmed_total_list = []
    confirmed_new_list = []
    death_total_list = []
    death_new_list = []
    last_updated_date_list = []
    for country_abbr in country_abbr_list:
        country_list.append(covid19_data[country_abbr]['location'])
        confirmed_total_list.append(covid19_data[country_abbr]['total_cases'])
        confirmed_new_list.append(covid19_data[country_abbr]['new_cases'])
        death_total_list.append(covid19_data[country_abbr]['total_deaths'])
        death_new_list.append(covid19_data[country_abbr]['new_deaths'])
        last_updated_date_list.append(covid19_data[country_abbr]['last_updated_date'])
    print(country_list)
    print(confirmed_total_list)
    
    #SQL语句
    query = "insert into covid19_table_confirmed_data (countryFullName, date, confirmedCount, confirmedIncr, deadCount, deadIncr) values (%s,%s,%s,%s,%s,%s)"
    selectquery = "SELECT * FROM covid19_table_confirmed_data WHERE countryFullName = %s and date = %s"
    for i in range(0,len(country_list)):
        #判断是否重复
        query_values = (country_list[i], last_updated_date_list[i])
        cursor.execute(selectquery, query_values)
        results = cursor.fetchall()
        #print(results)
        if results :
            print('该条已存在')
        else:
            values = (country_list[i], last_updated_date_list[i], confirmed_total_list[i]
            , confirmed_new_list[i], death_total_list[i], death_new_list[i])
            print(values)
            cursor.execute(query, values)
    # 提交
    cursor.close()
    db.commit()
    db.close()
    
    
def main(h=20, m=0):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        # 判断是否达到设定时间，例如23:00
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            if now.hour==h and now.minute==m:
                break
            # 不到时间就等20秒之后再次检测
            time.sleep(60)
        # 做正事，一天做一次
        WorldwideData()
    
if __name__ == '__main__':
    #main()
    WorldwideData()
    