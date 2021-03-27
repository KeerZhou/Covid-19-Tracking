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

#当前日期
time = time.strftime("%Y-%m-%d",time.localtime())

# 全球疫情数据
def WorldwideData():
    #url="https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/1/query?f=json&where=Country_Region%3D%27US%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc%2CCountry_Region%20asc%2CProvince_State%20asc&resultOffset=0&resultRecordCount=200&resultType=standard&cacheHint=true"
    #https://coronavirus.jhu.edu/map.html
    # 全世界各国数据
    url="https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/2/query?f=json&where=Recovered%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Recovered%20desc&resultOffset=0&resultRecordCount=250&resultType=standard&cacheHint=true"
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://www.arcgis.com/apps/opsdashboard/index.html'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    #print(resp)
    htmls = resp.read()
    #print(htmls)
    # 获取json
    jsonResponse = json.loads(htmls.decode('utf-8'))
    #print(jsonResponse)
    # 定位
    data = jsonResponse['features']
    # json长度
    #print(len(data))
    # 遍历输出
    for i in range(0,len(data)):
        case = data[i]['attributes']
        #print(case)
        print("国家：" + case['Country_Region']+" "+
              #"地区：" + case['Province_State']+" "
              "累计确诊：" + str(case['Confirmed'])+" "+
              "累计治愈：" + str(case['Recovered'])+" "+
              "累计死亡：" + str(case['Deaths'])+" "+
              "现有确诊：" + str(case['Active']) + " " +
              "发病率：" + str(case['Incident_Rate']) + " " +
              "死亡率：" + str(case['Mortality_Rate']))
        # print("地区：" + case['Province_State'])
        # print("累计确诊：" + str(case['Confirmed']))
        # print("恢复：" + str(case['Recovered']))
        # print("累计死亡：" + str(case['Deaths']))

    # buff = BytesIO(htmls)
    # f = gzip.GzipFile(fileobj=buff)
    # content = f.read().decode('utf-8','ignore')
    # print(content)
    #缩小范围（待优化）
    # res1 = r'"features":[(.*?)]}'
    # mm1 = re.findall(res1, htmls, re.S|re.M)
    # #for value in mm1:
    # print(mm1)

# 美国疫情数据
def USAData():
    # 美国各州数据
    #https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/1/query?f=json&where=Country_Region%3D%27US%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc%2CCountry_Region%20asc%2CProvince_State%20asc&resultOffset=0&resultRecordCount=200&resultType=standard&cacheHint=true
    #https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/3/query?f=json&where=Country_Region%3D%27US%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Deaths%20desc&outSR=102100&resultOffset=0&resultRecordCount=100&resultType=standard&cacheHint=true
    url = "https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/3/query?f=json&where=Country_Region%3D%27US%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Deaths%20desc&outSR=102100&resultOffset=0&resultRecordCount=100&resultType=standard&cacheHint=true"
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://www.arcgis.com/apps/opsdashboard/index.html'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    #print(resp)
    htmls = resp.read()
    #print(htmls)
    # 获取json
    jsonResponse = json.loads(htmls.decode('utf-8'))
    #print(jsonResponse)
    # 定位
    data = jsonResponse['features']
    # json长度
    #print(len(data))
    # 遍历输出
    for i in range(0,len(data)):
        case = data[i]['attributes']
        #print(case)
        print(#"国家：" + case['Country_Region']+" "+
              "地区：" + case['Province_State']+" "
              "累计确诊：" + str(case['Confirmed'])+" "+
              "累计治愈：" + str(case['Recovered'])+" "+
              "累计死亡：" + str(case['Deaths'])+" "+
              "现有确诊：" + str(case['Active']) + " " +
              "发病率：" + str(case['Incident_Rate'])+ " " +
              "死亡率：" + str(case['Mortality_Rate']))

#https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=225&resultType=standard&cacheHint=true
# 排序
def SortData():
    # 世界各国数据排序
    #https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=225&resultType=standard&cacheHint=true
    url = "https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=225&resultType=standard&cacheHint=true"
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://www.arcgis.com/apps/opsdashboard/index.html'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    #print(resp)
    htmls = resp.read()
    #print(htmls)
    # 获取json
    jsonResponse = json.loads(htmls.decode('utf-8'))
    #print(jsonResponse)
    # 定位
    data = jsonResponse['features']
    # json长度
    #print(len(data))
    # 遍历输出
    for i in range(0,len(data)):
        case = data[i]['attributes']
        #print(case)
        print("国家：" + case['Country_Region']+" "+
              #"地区：" + case['Province_State']+" "
              "累计确诊：" + str(case['Confirmed'])+" "+
              "累计治愈：" + str(case['Recovered'])+" "+
              "累计死亡：" + str(case['Deaths'])+" "+
              "现有确诊：" + str(case['Active']) + " " +
              "发病率：" + str(case['Incident_Rate'])+ " " +
              "死亡率：" + str(case['Mortality_Rate']))

def test():
    url = "https://www.baidu.com"
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Referer':'https://www.arcgis.com/apps/opsdashboard/index.html'
    }
    req = request.Request(url,headers=headers)
    resp = request.urlopen(req)
    #print(resp)
    htmls = resp.read()
    print(htmls)

if __name__ == '__main__':
    #WorldwideData()
    #USAData()
    SortData()
    #test()