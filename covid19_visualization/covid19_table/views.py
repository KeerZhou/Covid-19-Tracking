from django.shortcuts import render
#视图处理
# Create your views here.
import json
import random
import numpy as np
from django.shortcuts import render
from django.shortcuts import  HttpResponse
from covid19_table.models import Article
from covid19_table.models import News
from covid19_table.models import Research
from covid19_table.models import Predict_result
from covid19_table.models import Confirmed_data
from django.db import connection
from datetime import date, timedelta
from django.core.paginator import Paginator
from covid19_table.SIR_model import SIR_model,SEIR_model,RMIL_model

def getYesterday():
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    return yesterday

# 将请求定位到index.html文件中
def index(request):
    return render(request,'index.html')

# 将请求定位到world.html文件中
def world(request):
    return render(request,'world.html')


def hellow_world(request):
    return HttpResponse("Hello World")

# def article_content(request):
#     article = Article.objects.all()[0]
#     title = article.title
#     content = article.content
#     publish_date = article.publish_date
#     return_str = 'title:%s,content:%s,publish_date:%s'%(title,content,publish_date)

    return HttpResponse(return_str)


# 将请求定位到assessment_index.html文件中
def get_assessment_inedx(request):
    cityname_list = Predict_result.objects.values('cityName').distinct()
    citynum = range(1,len(cityname_list)+1)
    city_photo = ['NY','SD','NJ','VA']
    #预测图片
    city_list = zip(citynum, cityname_list, city_photo)
    return render(request, 'assessment/assessment_index.html',
                  {
                    'city_list':city_list,
                  })


# 将请求定位到assessment_detail.html文件中
def get_assessment_detail(request, cityName):
    # all_article = Article.objects.all()
    # #文章发布时间格式
    # for article in all_article:
    #     article.publish_date = replace_date(article.publish_date)
    # for article in all_article:
    #     if article.article_id == article_id:
    #         curr_article = article
    #         break
    # section_list = curr_article.content.split('\n')
    # author = curr_article.author
    # source = curr_article.source
    # publish_date = curr_article.publish_date
    if cityName == 'New York':
        NY_sql = "SELECT predict_result_id,date,confirmedCount,confirmedIncr,pre_confirmedCount,pre_confirmedIncr FROM covid19_table_predict_result WHERE cityName = 'New York' and omega = '0.22'"
        NY_predict_result = get_predict_result_list(NY_sql)
        predict_result = NY_predict_result
        omega_list = [0.2,0.22,0.25,0.3]
    elif cityName == 'South Dakota':
        SD_sql = "SELECT predict_result_id,date,confirmedCount,confirmedIncr,pre_confirmedCount,pre_confirmedIncr FROM covid19_table_predict_result WHERE cityName = 'South Dakota' and omega = '0.056'"
        SD_predict_result = get_predict_result_list(SD_sql)
        predict_result = SD_predict_result
        omega_list = [0.05, 0.056, 0.06, 0.065]
    elif cityName == 'New Jersey':
        NJ_sql = "SELECT predict_result_id,date,confirmedCount,confirmedIncr,pre_confirmedCount,pre_confirmedIncr FROM covid19_table_predict_result WHERE cityName = 'New Jersey' and omega = '0.14'"
        NJ_predict_result = get_predict_result_list(NJ_sql)
        predict_result = NJ_predict_result
        omega_list = [0.13, 0.14, 0.15, 0.16]
    elif cityName == 'Virginia':
        VA_sql = "SELECT predict_result_id,date,confirmedCount,confirmedIncr,pre_confirmedCount,pre_confirmedIncr FROM covid19_table_predict_result WHERE cityName = 'Virginia' and omega = '0.19'"
        VA_predict_result = get_predict_result_list(VA_sql)
        predict_result = VA_predict_result
        omega_list = [0.18, 0.19, 0.20, 0.21]

    return render(request, 'assessment/assessment_detail.html',
                  {
                    'cityName':cityName,
                    'predict_result' : json.dumps(predict_result),
                    'omega_list' : omega_list,
                  }
                 )

#改变omega获取预测结果
def get_omega_result(request):
    omega = request.GET.get('omega')
    cityName = request.GET.get('cityName')
    sql = "SELECT predict_result_id,date,confirmedCount,confirmedIncr,pre_confirmedCount,pre_confirmedIncr FROM covid19_table_predict_result WHERE cityName = '" + cityName + "' and omega = '" + omega + "'"
    predict_result = get_predict_result_list(sql)
    res = {'pre_confirmedCount': predict_result[3],'pre_confirmedIncr': predict_result[4]}
    return HttpResponse(json.dumps(res))


# 将请求定位到research.html文件中
def get_research_page(request):
    all_research = Research.objects.all()
    #研究发布时间格式
    for research in all_research:
        research.publish_date = replace_date(research.publish_date)[:4]
    for research in all_research:
        research.research_url = research.research_title[:4]
    return render(request, 'research/research_index.html',
                  {
                        'research_list': all_research,
                  })

# 将请求定位到news.html文件中
def get_news_page(request):
    all_news = News.objects.all()
    cage_num = range(1,17)
    #新闻来源
    news_source_list = News.objects.values('source').distinct()

    #按时间排序
    time_sort = request.GET.get('time_sort')
    if time_sort == 'desc':
        time_sort_name = '由晚到早'
    elif time_sort == 'asc':
        time_sort_name = '由早到晚'
    else:
        time_sort_name = '默认排序'
    top_news_list_desc = News.objects.all().order_by('-publish_date')
    top_news_list_asc = News.objects.all().order_by('publish_date')
    if time_sort == 'desc':
        all_news = top_news_list_desc
    elif time_sort == 'asc':
        all_news = top_news_list_asc
    else:
        all_news = top_news_list_desc

    #按来源分类
    news_source = request.GET.get('source')
    if news_source:
        source_name = news_source
    else:
        source_name = '默认来源'

    if news_source:
        if news_source == '默认来源':
            all_news = News.objects.all()
            time_sort = request.GET.get('time_sort')
            top_news_list_desc = News.objects.all().order_by('-publish_date')
            top_news_list_asc = News.objects.all().order_by('publish_date')
            if time_sort == 'desc':
                all_news = top_news_list_desc
            elif time_sort == 'asc':
                all_news = top_news_list_asc
            else:
                all_news = top_news_list_desc
        elif news_source == 'None':
            top_news_list_desc = News.objects.all().order_by('-publish_date')
            all_news = top_news_list_desc
            source_name = '默认来源'
        else:
            all_news = News.objects.filter(source=news_source)
            time_sort = request.GET.get('time_sort')
            source_top_news_list_desc = News.objects.filter(source=news_source).order_by('-publish_date')
            source_top_news_list_asc = News.objects.filter(source=news_source).order_by('publish_date')
            if time_sort == 'desc':
                all_news = source_top_news_list_desc
            elif time_sort == 'asc':
                all_news = source_top_news_list_asc
            else:
                all_news = News.objects.filter(source=news_source)
    else:
        all_news = top_news_list_desc

    #新闻发布时间格式
    for news in all_news:
        news.publish_date = replace_date(news.publish_date)

    #新闻图片
    for news in all_news:
        if "疫苗" in news.news_title:
            news.news_photo_index = 'vaccines/' + str(random.randint(1, 17))
        else:
            news.news_photo_index = 'virus/' + str(random.randint(1, 17))

    #设置分页
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    #print(page)
    paginator = Paginator(all_news,16)
    page_num = paginator.num_pages
    page_news_list = paginator.page(page)
    if page_news_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_news_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page


    news_list = zip(cage_num,page_news_list)

    return render(request,'news/news_index.html',
                  {
                      'cage_num':cage_num,
                      'news_list': news_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'news_num': len(all_news),
                      'time_sort':time_sort,
                      'news_source_list':news_source_list,
                      'source':news_source,
                      'source_name':source_name,
                      'time_sort_name':time_sort_name

                    })

# 将请求定位到article.html文件中
def get_inedx_page(request):
    all_article = Article.objects.all()
    #按时间排序
    time_sort = request.GET.get('time_sort')
    if time_sort == 'desc':
        time_sort_name = '由晚到早'
    elif time_sort == 'asc':
        time_sort_name = '由早到晚'
    else:
        time_sort_name = '默认排序'
    top_article_list_desc = Article.objects.order_by('-publish_date')
    top_article_list_asc = Article.objects.order_by('publish_date')
    if time_sort == 'desc':
        all_article = top_article_list_desc
    elif time_sort == 'asc':
        all_article = top_article_list_asc
    else:
        all_article = Article.objects.all()
    #最新文章
    top5_article_list = Article.objects.order_by('publish_date')[:5]
    #文章来源
    article_source_list = Article.objects.values('source').distinct()
    #文章发布时间格式
    for article in all_article:
        article.publish_date = replace_date(article.publish_date)
    #设置分页
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    #print(page)
    paginator = Paginator(all_article,6)
    page_num = paginator.num_pages
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'article/article.html',
                    {
                      'article_list':page_article_list,
                      'page_num': range(1,page_num + 1),
                      'curr_page':page,
                      'next_page':next_page,
                      'previous_page':previous_page,
                      'top5_article_list':top5_article_list,
                      'article_source_list':article_source_list,
                      'article_num':len(all_article),
                      'time_sort': time_sort,
                      'time_sort_name': time_sort_name

                    }
                  )

# 将请求定位到article_detail.html文件中
def get_detail_page(request, article_id):
    all_article = Article.objects.all()
    #文章发布时间格式
    for article in all_article:
        article.publish_date = replace_date(article.publish_date)
    for article in all_article:
        if article.article_id == article_id:
            curr_article = article
            break
    section_list = curr_article.content.split('\n')
    author = curr_article.author
    source = curr_article.source
    publish_date = curr_article.publish_date
    return render(request, 'article/article_detail.html',
                  {
                      'curr_article':curr_article,
                      'section_list':section_list,
                      'author':author,
                      'source':source,
                      'publish_date':publish_date

                  }
                 )

# 将请求定位到index.html文件中
def get_confirmed_data(request):
    updatetime = getYesterday();
    # 2020-02 -- 2020-12 确诊数据
    sql0215 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-02-15'"
    confirmed_data_list0215 = get_monthpositive_data(sql0215)

    sql0315 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-03-15'"
    confirmed_data_list0315 = get_monthpositive_data(sql0315)

    sql0415 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-04-15'"
    confirmed_data_list0415 = get_monthpositive_data(sql0415)

    sql0515 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-05-15'"
    confirmed_data_list0515 = get_monthpositive_data(sql0515)

    sql0615 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-06-15'"
    confirmed_data_list0615 = get_monthpositive_data(sql0615)

    sql0715 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-07-15'"
    confirmed_data_list0715 = get_monthpositive_data(sql0715)

    sql0815 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-08-15'"
    confirmed_data_list0815 = get_monthpositive_data(sql0815)

    sql0915 = "SELECT id,countryName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-09-16'"
    confirmed_data_list0915 = get_monthpositive_data(sql0915)

    sql1015 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-10-16'"
    confirmed_data_list1015 = get_monthpositive_data(sql1015)

    sql1115 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-11-15'"
    confirmed_data_list1115 = get_monthpositive_data(sql1115)

    sql1215 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2020-12-15'"
    confirmed_data_list1215 = get_monthpositive_data(sql1215)

    sql210115 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2021-01-15'"
    confirmed_data_list210115 = get_monthpositive_data(sql210115)

    sql210215 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date='2021-02-15'"
    confirmed_data_list210215 = get_monthpositive_data(sql210215)

    sql210301 = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date=date_sub(curdate(),interval 2 day);"
    confirmed_data_list210301 = get_monthpositive_data(sql210301)

    #全球累计确诊人数
    confirmed_sum_sql = "SELECT sum(confirmedIncr) FROM covid19_table_confirmed_data WHERE countryFullName = 'world'"
    confirmed_sum = get_allpositive_data(confirmed_sum_sql)

    #全球新增确诊人数
    confirmed_increase_sql = "SELECT confirmedIncr FROM covid19_table_confirmed_data WHERE countryFullName = 'world' ORDER BY id DESC LIMIT 1"
    confirmed_increase = get_allpositive_data(confirmed_increase_sql)

    #全球累计死亡人数
    death_sum_sql = "SELECT sum(deadIncr) FROM covid19_table_confirmed_data WHERE countryFullName = 'world'"
    death_sum = get_allpositive_data(death_sum_sql)

    #全球新增死亡人数
    death_increase_sql = "SELECT deadIncr FROM covid19_table_confirmed_data WHERE countryFullName = 'world' ORDER BY id DESC LIMIT 1"
    death_increase = get_allpositive_data(death_increase_sql)

    # 全球新增确诊人数排名
    confirmed_increase_order_sql = "SELECT id,countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date=date_sub(curdate(),interval 2 day) ORDER BY confirmedIncr DESC LIMIT 26"
    confirmed_increase_order = get_positive_data_order(confirmed_increase_order_sql)
    #confirmed_increase_order = {'name':'american','value':1000}
    #fielddict = {'name': '张三', 'age': 18}

    #英国确诊人数变化总计
    confirmed_grow_list_UK_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United Kingdom' and date > '2020-02-31'"
    confirmed_grow_list_UK = get_grow_list(confirmed_grow_list_UK_sql)

    #美国确诊人数变化总计
    confirmed_grow_list_USA_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United States' and date > '2020-02-31'"
    confirmed_grow_list_USA = get_grow_list(confirmed_grow_list_USA_sql)

    #中国确诊人数变化总计
    confirmed_grow_list_CHN_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='China' and date > '2020-02-31'"
    confirmed_grow_list_CHN = get_grow_list(confirmed_grow_list_CHN_sql)

    #印度确诊人数变化总计
    confirmed_grow_list_IND_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='India' and date > '2020-02-31'"
    confirmed_grow_list_IND = get_grow_list(confirmed_grow_list_IND_sql)

    #意大利确诊人数变化总计
    confirmed_grow_list_ITA_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Italy' and date > '2020-02-31'"
    confirmed_grow_list_ITA = get_grow_list(confirmed_grow_list_ITA_sql)

    #俄罗斯确诊人数变化总计
    confirmed_grow_list_RUS_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Russia' and date > '2020-02-31'"
    confirmed_grow_list_RUS = get_grow_list(confirmed_grow_list_RUS_sql)

    #巴西确诊人数变化总计
    confirmed_grow_list_BRA_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Brazil' and date > '2020-02-31'"
    confirmed_grow_list_BRA = get_grow_list(confirmed_grow_list_BRA_sql)


    #90天
    # 美国近90天新增确诊人数
    confirmed_increase_USA_90_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United States' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_increase_USA_90 = get_incr_list(confirmed_increase_USA_90_sql)

    # 美国近90天累计确诊人数
    confirmed_accumulative_USA_90_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United States' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_accumulative_USA_90 = get_grow_list(confirmed_accumulative_USA_90_sql)

    # 美国近90天新增死亡人数
    dead_increase_USA_90_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United States' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    dead_increase_USA_90 = get_dead_list(dead_increase_USA_90_sql)

    # 英国近90天新增确诊人数
    confirmed_increase_UK_90_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United Kingdom' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_increase_UK_90 = get_incr_list(confirmed_increase_UK_90_sql)

    # 英国近90天累计确诊人数
    confirmed_accumulative_UK_90_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United Kingdom' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_accumulative_UK_90 = get_grow_list(confirmed_accumulative_UK_90_sql)

    # 英国近90天新增死亡人数
    dead_increase_UK_90_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United Kingdom' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    dead_increase_UK_90 = get_dead_list(dead_increase_UK_90_sql)

    # 中国近90天新增确诊人数
    confirmed_increase_CHN_90_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='China' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_increase_CHN_90 = get_incr_list(confirmed_increase_CHN_90_sql)

    # 中国近90天累计确诊人数
    confirmed_accumulative_CHN_90_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='China' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_accumulative_CHN_90 = get_grow_list(confirmed_accumulative_CHN_90_sql)

    # 中国近90天新增死亡人数
    dead_increase_CHN_90_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='China' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    dead_increase_CHN_90 = get_dead_list(dead_increase_CHN_90_sql)

    # 巴西近90天新增确诊人数
    confirmed_increase_BRA_90_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Brazil' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_increase_BRA_90 = get_incr_list(confirmed_increase_BRA_90_sql)

    # 巴西近90天累计确诊人数
    confirmed_accumulative_BRA_90_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Brazil' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_accumulative_BRA_90 = get_grow_list(confirmed_accumulative_BRA_90_sql)

    # 巴西近90天新增死亡人数
    dead_increase_BRA_90_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Brazil' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    dead_increase_BRA_90 = get_dead_list(dead_increase_BRA_90_sql)

    # 印度近90天新增确诊人数
    confirmed_increase_IND_90_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='India' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_increase_IND_90 = get_incr_list(confirmed_increase_IND_90_sql)

    # 印度近90天累计确诊人数
    confirmed_accumulative_IND_90_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='India' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_accumulative_IND_90 = get_grow_list(confirmed_accumulative_IND_90_sql)

    # 印度近90天新增死亡人数
    dead_increase_IND_90_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='India' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    dead_increase_IND_90 = get_dead_list(dead_increase_IND_90_sql)

    # 俄罗斯近90天新增确诊人数
    confirmed_increase_RUS_90_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Russia' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_increase_RUS_90 = get_incr_list(confirmed_increase_RUS_90_sql)

    # 俄罗斯近90天累计确诊人数
    confirmed_accumulative_RUS_90_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Russia' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    confirmed_accumulative_RUS_90 = get_grow_list(confirmed_accumulative_RUS_90_sql)

    # 俄罗斯近90天新增死亡人数
    dead_increase_RUS_90_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Russia' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 90 DAY) <= date"
    dead_increase_RUS_90 = get_dead_list(dead_increase_RUS_90_sql)




    #14天
    # 美国近14天新增确诊人数
    confirmed_increase_USA_14_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United States' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_increase_USA_14 = get_incr_list(confirmed_increase_USA_14_sql)

    # 美国近14天累计确诊人数
    confirmed_accumulative_USA_14_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United States' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_accumulative_USA_14 = get_grow_list(confirmed_accumulative_USA_14_sql)

    # 美国近14天新增死亡人数
    dead_increase_USA_14_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United States' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    dead_increase_USA_14 = get_dead_list(dead_increase_USA_14_sql)


    # 英国近14天新增确诊人数
    confirmed_increase_UK_14_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United Kingdom' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_increase_UK_14 = get_incr_list(confirmed_increase_UK_14_sql)

    # 英国近14天累计确诊人数
    confirmed_accumulative_UK_14_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United Kingdom' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_accumulative_UK_14 = get_grow_list(confirmed_accumulative_UK_14_sql)

    # 英国近14天新增死亡人数
    dead_increase_UK_14_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='United Kingdom' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    dead_increase_UK_14 = get_dead_list(dead_increase_UK_14_sql)

    # 中国近14天新增确诊人数
    confirmed_increase_CHN_14_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='China' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_increase_CHN_14 = get_incr_list(confirmed_increase_CHN_14_sql)

    # 中国近14天累计确诊人数
    confirmed_accumulative_CHN_14_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='China' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_accumulative_CHN_14 = get_grow_list(confirmed_accumulative_CHN_14_sql)

    # 中国近14天新增死亡人数
    dead_increase_CHN_14_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='China' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    dead_increase_CHN_14 = get_dead_list(dead_increase_CHN_14_sql)

    # 巴西近14天新增确诊人数
    confirmed_increase_BRA_14_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Brazil' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_increase_BRA_14 = get_incr_list(confirmed_increase_BRA_14_sql)

    # 巴西近14天累计确诊人数
    confirmed_accumulative_BRA_14_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Brazil' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_accumulative_BRA_14 = get_grow_list(confirmed_accumulative_BRA_14_sql)

    # 巴西近14天新增死亡人数
    dead_increase_BRA_14_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Brazil' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    dead_increase_BRA_14 = get_dead_list(dead_increase_BRA_14_sql)

    # 印度近14天新增确诊人数
    confirmed_increase_IND_14_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='India' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_increase_IND_14 = get_incr_list(confirmed_increase_IND_14_sql)

    # 印度近14天累计确诊人数
    confirmed_accumulative_IND_14_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='India' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_accumulative_IND_14 = get_grow_list(confirmed_accumulative_IND_14_sql)

    # 印度近14天新增死亡人数
    dead_increase_IND_14_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='India' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    dead_increase_IND_14 = get_dead_list(dead_increase_IND_14_sql)

    # 俄罗斯近14天新增确诊人数
    confirmed_increase_RUS_14_sql = "SELECT id,date,confirmedIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Russia' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_increase_RUS_14 = get_incr_list(confirmed_increase_RUS_14_sql)

    # 俄罗斯近14天累计确诊人数
    confirmed_accumulative_RUS_14_sql = "SELECT id,date,confirmedCount,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Russia' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    confirmed_accumulative_RUS_14 = get_grow_list(confirmed_accumulative_RUS_14_sql)

    # 俄罗斯近14天新增死亡人数
    dead_increase_RUS_14_sql = "SELECT id,date,deadIncr,countryFullName FROM covid19_table_confirmed_data WHERE countryFullName='Russia' and DATE_SUB((select max(date) FROM covid19_table_confirmed_data), INTERVAL 13 DAY) <= date"
    dead_increase_RUS_14 = get_dead_list(dead_increase_RUS_14_sql)



    return render(request, 'index.html',
                  {
                      'updatetime' : updatetime,
                      'confirmed_data_list0215' : json.dumps(confirmed_data_list0215),
                      'confirmed_data_list0315' : json.dumps(confirmed_data_list0315),
                      'confirmed_data_list0415' : json.dumps(confirmed_data_list0415),
                      'confirmed_data_list0515' : json.dumps(confirmed_data_list0515),
                      'confirmed_data_list0615' : json.dumps(confirmed_data_list0615),
                      'confirmed_data_list0715' : json.dumps(confirmed_data_list0715),
                      'confirmed_data_list0815' : json.dumps(confirmed_data_list0815),
                      'confirmed_data_list0915' : json.dumps(confirmed_data_list0915),
                      'confirmed_data_list1015' : json.dumps(confirmed_data_list1015),
                      'confirmed_data_list1115' : json.dumps(confirmed_data_list1115),
                      'confirmed_data_list1215' : json.dumps(confirmed_data_list1215),
                      'confirmed_data_list210115' : json.dumps(confirmed_data_list210115),
                      'confirmed_data_list210215' : json.dumps(confirmed_data_list210215),
                      'confirmed_data_list210301': json.dumps(confirmed_data_list210301),
                      'confirmed_increase_order': confirmed_increase_order,
                      'confirmed_sum' : confirmed_sum,
                      'confirmed_increase' : confirmed_increase,
                      'death_sum': death_sum,
                      'death_increase': death_increase,
                      'UK_date' : json.dumps(confirmed_grow_list_UK[0]),
                      'UK_confirmed' : json.dumps(confirmed_grow_list_UK[1]),
                      'USA_confirmed': json.dumps(confirmed_grow_list_USA[1]),
                      'IND_confirmed': json.dumps(confirmed_grow_list_IND[1]),
                      'CHN_confirmed': json.dumps(confirmed_grow_list_CHN[1]),
                      'ITA_confirmed': json.dumps(confirmed_grow_list_ITA[1]),
                      'RUS_confirmed': json.dumps(confirmed_grow_list_RUS[1]),
                      'BRA_confirmed': json.dumps(confirmed_grow_list_BRA[1]),

                      'USA_date_90': json.dumps(confirmed_increase_USA_90[0]),
                      'USA_confirmed_incr_90' : json.dumps(confirmed_increase_USA_90[1]),
                      'USA_confirmed_accu_90': json.dumps(confirmed_accumulative_USA_90[1]),
                      'USA_dead_incr_90': json.dumps(dead_increase_USA_90[1]),
                      'UK_confirmed_incr_90': json.dumps(confirmed_increase_UK_90[1]),
                      'UK_confirmed_accu_90': json.dumps(confirmed_accumulative_UK_90[1]),
                      'UK_dead_incr_90': json.dumps(dead_increase_UK_90[1]),
                      'CHN_confirmed_incr_90': json.dumps(confirmed_increase_CHN_90[1]),
                      'CHN_confirmed_accu_90': json.dumps(confirmed_accumulative_CHN_90[1]),
                      'CHN_dead_incr_90': json.dumps(dead_increase_CHN_90[1]),
                      'BRA_confirmed_incr_90': json.dumps(confirmed_increase_BRA_90[1]),
                      'BRA_confirmed_accu_90': json.dumps(confirmed_accumulative_BRA_90[1]),
                      'BRA_dead_incr_90': json.dumps(dead_increase_BRA_90[1]),
                      'IND_confirmed_incr_90': json.dumps(confirmed_increase_IND_90[1]),
                      'IND_confirmed_accu_90': json.dumps(confirmed_accumulative_IND_90[1]),
                      'IND_dead_incr_90': json.dumps(dead_increase_IND_90[1]),
                      'RUS_confirmed_incr_90': json.dumps(confirmed_increase_RUS_90[1]),
                      'RUS_confirmed_accu_90': json.dumps(confirmed_accumulative_RUS_90[1]),
                      'RUS_dead_incr_90': json.dumps(dead_increase_RUS_90[1]),


                      'USA_date_14': json.dumps(confirmed_increase_USA_14[0]),
                      'USA_confirmed_incr_14': json.dumps(confirmed_increase_USA_14[1]),
                      'USA_confirmed_accu_14': json.dumps(confirmed_accumulative_USA_14[1]),
                      'USA_dead_incr_14': json.dumps(dead_increase_USA_14[1]),
                      'UK_date_14': json.dumps(confirmed_increase_UK_14[0]),
                      'UK_confirmed_incr_14': json.dumps(confirmed_increase_UK_14[1]),
                      'UK_confirmed_accu_14': json.dumps(confirmed_accumulative_UK_14[1]),
                      'UK_dead_incr_14': json.dumps(dead_increase_UK_14[1]),
                      'CHN_date_14': json.dumps(confirmed_increase_CHN_14[0]),
                      'CHN_confirmed_incr_14': json.dumps(confirmed_increase_CHN_14[1]),
                      'CHN_confirmed_accu_14': json.dumps(confirmed_accumulative_CHN_14[1]),
                      'CHN_dead_incr_14': json.dumps(dead_increase_CHN_14[1]),
                      'BRA_date_14': json.dumps(confirmed_increase_BRA_14[0]),
                      'BRA_confirmed_incr_14': json.dumps(confirmed_increase_BRA_14[1]),
                      'BRA_confirmed_accu_14': json.dumps(confirmed_accumulative_BRA_14[1]),
                      'BRA_dead_incr_14': json.dumps(dead_increase_BRA_14[1]),
                      'IND_date_14': json.dumps(confirmed_increase_IND_14[0]),
                      'IND_confirmed_incr_14': json.dumps(confirmed_increase_IND_14[1]),
                      'IND_confirmed_accu_14': json.dumps(confirmed_accumulative_IND_14[1]),
                      'IND_dead_incr_14': json.dumps(dead_increase_IND_14[1]),
                      'RUS_confirmed_incr_14': json.dumps(confirmed_increase_RUS_14[1]),
                      'RUS_confirmed_accu_14': json.dumps(confirmed_accumulative_RUS_14[1]),
                      'RUS_dead_incr_14': json.dumps(dead_increase_RUS_14[1]),

                      # 'countryname':countryname,
                      # 'confirmednum':confirmednum
                  }
                 )

#查询人数
def get_allpositive_data(sql):
    cur = connection.cursor()
    cur.execute(sql)
    confirmed_num = cur.fetchall()[0][0]
    confirmed_num = format(confirmed_num,',')
    return confirmed_num


def get_monthpositive_data(sql):
    confirmed_data = Confirmed_data.objects.raw(sql)
    json_data = {}
    data_list = []
    for obj in confirmed_data:
        data = {}  # 要在遍历里面创建字典用于存数据
        #print(obj)
        data["id"] = obj.id
        if obj.countryFullName == 'Russian Federation':
            obj.countryFullName = 'Russia'
        if obj.countryFullName == 'United States of America':
            obj.countryFullName = 'United States'
        if obj.countryFullName == 'Iran (Islamic Republic of)':
            obj.countryFullName = 'Iran'
        if obj.countryFullName == 'Bolivia (Plurinational State of)':
            obj.countryFullName = 'Bolivia'
        if obj.countryFullName == 'South Korea':
            obj.countryFullName = 'Korea'
        if obj.countryFullName == 'Republic of Korea':
            obj.countryFullName = 'Korea'
        if obj.countryFullName == 'The United Kingdom':
            obj.countryFullName = 'United Kingdom'
        if obj.countryFullName == 'The Republic of Zambia':
            obj.countryFullName = 'Zambia'
        if obj.countryFullName == 'South Sudan':
            obj.countryFullName = 'S. Sudan'
        if obj.countryFullName == 'The Republic of Yemen':
            obj.countryFullName = 'Yemen'
        if obj.countryFullName == 'Central African Repu':
            obj.countryFullName = 'Central African Rep.'
        if obj.countryFullName == 'Czechia':
            obj.countryFullName = 'Czech Rep.'
        if obj.countryFullName == 'Bosnia and Herzegovi':
            obj.countryFullName = 'Bosnia and Herz.'
        if obj.countryFullName == 'North Macedonia':
            obj.countryFullName = 'Macedonia'
        if obj.countryFullName == "Cote d'Ivoire":
            obj.countryFullName = "CÃ´te d'Ivoire"
        if obj.countryFullName == 'World':
            continue
        if obj.countryFullName == 'International':
            continue
        if obj.countryFullName == 'Europe':
            continue
        if obj.countryFullName == 'North America':
            continue
        if obj.countryFullName == 'European Union':
            continue
        if obj.countryFullName == 'South America':
            continue
        if obj.countryFullName == 'Asia':
            continue
        if obj.countryFullName == 'Africa':
            continue
        if obj.countryFullName == 'Oceania':
            continue
        data["countryFullName"] = replace_chinese(obj.countryFullName)
        data["confirmedIncr"] = obj.confirmedIncr
        data_list.append(data)
    #json_data['data'] = data_list
    confirmed_data_list = []
    for i in range(0,len(data_list)):
        temp = {'name':data_list[i]["countryFullName"], 'value':data_list[i]["confirmedIncr"]}
        confirmed_data_list.append(temp)
    return confirmed_data_list

#查询中文
def get_chinesemonthpositive_data(sql):
    confirmed_data = Confirmed_data.objects.raw(sql)
    json_data = {}
    data_list = []
    for obj in confirmed_data:
        data = {}  # 要在遍历里面创建字典用于存数据
        #print(obj)
        data["id"] = obj.id
        data["countryName"] = obj.countryName
        data["confirmedIncr"] = obj.confirmedIncr
        data_list.append(data)
    #json_data['data'] = data_list
    confirmed_data_list = []
    for i in range(0,len(data_list)):
        temp = {'name':data_list[i]["countryName"], 'value':data_list[i]["confirmedIncr"]}
        confirmed_data_list.append(temp)
    return confirmed_data_list


#获取国家确诊人数排名
def get_positive_data_order(sql):
    confirmed_data = Confirmed_data.objects.raw(sql)
    json_data = {}
    data_list = []
    for obj in confirmed_data:
        data = {}  # 要在遍历里面创建字典用于存数据
        #print(obj)
        data["id"] = obj.id
        if obj.countryFullName == 'Russian Federation':
            obj.countryFullName = 'Russia'
        if obj.countryFullName == 'United States of America':
            obj.countryFullName = 'United States'
        if obj.countryFullName == 'Iran (Islamic Republic of)':
            obj.countryFullName = 'Iran'
        if obj.countryFullName == 'Congo':
            obj.countryFullName = 'Dem. Rep. Congo'
        if obj.countryFullName == 'Bolivia (Plurinational State of)':
            obj.countryFullName = 'Bolivia'
        if obj.countryFullName == 'South Korea':
            obj.countryFullName = 'Korea'
        if obj.countryFullName == 'Republic of Korea':
            obj.countryFullName = 'Korea'
        if obj.countryFullName == 'The United Kingdom':
            obj.countryFullName = 'United Kingdom'
        if obj.countryFullName == 'The Republic of Zambia':
            obj.countryFullName = 'Zambia'
        if obj.countryFullName == 'South Sudan':
            obj.countryFullName = 'S. Sudan'
        if obj.countryFullName == 'The Republic of Yemen':
            obj.countryFullName = 'Yemen'
        if obj.countryFullName == 'Central African Repu':
            obj.countryFullName = 'Central African Rep.'
        if obj.countryFullName == 'Czechia':
            obj.countryFullName = 'Czech Rep.'
        if obj.countryFullName == 'Bosnia and Herzegovi':
            obj.countryFullName = 'Bosnia and Herz.'
        if obj.countryFullName == 'North Macedonia':
            obj.countryFullName = 'Macedonia'
        if obj.countryFullName == 'World':
            continue
        if obj.countryFullName == 'World':
            continue
        if obj.countryFullName == 'Europe':
            continue
        if obj.countryFullName == 'North America':
            continue
        if obj.countryFullName == 'European Union':
            continue
        if obj.countryFullName == 'South America':
            continue
        if obj.countryFullName == 'Asia':
            continue
        if obj.countryFullName == 'Africa':
            continue
        if obj.countryFullName == 'Oceania':
            continue
        data["countryFullName"] = replace_chinese(obj.countryFullName)
        data["confirmedIncr"] = obj.confirmedIncr
        data_list.append(data)
    #json_data['data'] = data_list
    confirmed_data_list = {}
    for i in range(0,len(data_list)):
        confirmed_data_list[data_list[i]["countryFullName"]] = format(data_list[i]["confirmedIncr"],',')
        #temp = {'name':data_list[i]["countryFullName"], 'value':data_list[i]["confirmedIncr"]}
        #confirmed_data_list.append(temp)
    return confirmed_data_list


#获取国家确诊人数增长情况
def get_grow_list(sql):
    confirmed_data = Confirmed_data.objects.raw(sql)
    #json_data = {}
    data_list = []
    for obj in confirmed_data:
        data = {}  # 要在遍历里面创建字典用于存数据
        #print(obj)
        data["id"] = obj.id
        data["countryFullName"] = replace_chinese(obj.countryFullName)
        data["date"] = obj.date
        data["confirmedCount"] = obj.confirmedCount
        data_list.append(data)
    time_list = []
    confirmed_data_list = []
    for i in range(0, len(data_list)):
        confirmed_data_list.append(data_list[i]["confirmedCount"])
        time_list.append(replace_date(data_list[i]["date"]))

        # datetemp = {'date':data_list[i]["date"]}
        # confirmed_data = {'value': data_list[i]["confirmedCount"]}
        # time_list.append(datetemp)
        # confirmed_data_list.append(confirmed_data)
    return time_list,confirmed_data_list


#获取国家新增确诊人数增长情况
def get_incr_list(sql):
    confirmed_data = Confirmed_data.objects.raw(sql)
    #json_data = {}
    data_list = []
    for obj in confirmed_data:
        data = {}  # 要在遍历里面创建字典用于存数据
        #print(obj)
        data["id"] = obj.id
        data["countryFullName"] = replace_chinese(obj.countryFullName)
        data["date"] = obj.date
        data["confirmedIncr"] = obj.confirmedIncr
        data_list.append(data)
    time_list = []
    confirmed_data_list = []
    for i in range(0, len(data_list)):
        confirmed_data_list.append(data_list[i]["confirmedIncr"])
        time_list.append(replace_date(data_list[i]["date"]))

        # datetemp = {'date':data_list[i]["date"]}
        # confirmed_data = {'value': data_list[i]["confirmedCount"]}
        # time_list.append(datetemp)
        # confirmed_data_list.append(confirmed_data)
    return time_list,confirmed_data_list


#获取国家新增死亡人数增长情况
def get_dead_list(sql):
    confirmed_data = Confirmed_data.objects.raw(sql)
    #json_data = {}
    data_list = []
    for obj in confirmed_data:
        data = {}  # 要在遍历里面创建字典用于存数据
        #print(obj)
        data["id"] = obj.id
        data["countryFullName"] = replace_chinese(obj.countryFullName)
        data["date"] = obj.date
        data["deadIncr"] = obj.deadIncr
        data_list.append(data)
    time_list = []
    confirmed_data_list = []
    for i in range(0, len(data_list)):
        confirmed_data_list.append(data_list[i]["deadIncr"])
        time_list.append(replace_date(data_list[i]["date"]))

        # datetemp = {'date':data_list[i]["date"]}
        # confirmed_data = {'value': data_list[i]["confirmedCount"]}
        # time_list.append(datetemp)
        # confirmed_data_list.append(confirmed_data)
    return time_list,confirmed_data_list


#查询预测结果
def get_predict_result_list(sql):
    predict_result = Predict_result.objects.raw(sql)
    data_list = []
    for obj in predict_result:
        data = {}  # 要在遍历里面创建字典用于存数据
        data["predict_result_id"] = obj.predict_result_id
        data["date"] = obj.date
        data["confirmedCount"] = obj.confirmedCount
        data["confirmedIncr"] = obj.confirmedIncr
        data["pre_confirmedCount"] = obj.pre_confirmedCount
        data["pre_confirmedIncr"] = obj.pre_confirmedIncr
        data_list.append(data)
    time_list = []
    confirmedCount_list = []
    confirmedIncr_list = []
    pre_confirmedCount_list = []
    pre_confirmedIncr_list = []
    for i in range(0, len(data_list)):
        time_list.append(replace_date(data_list[i]["date"]))
        confirmedCount_list.append(data_list[i]["confirmedCount"])
        confirmedIncr_list.append(data_list[i]["confirmedIncr"])
        pre_confirmedCount_list.append(data_list[i]["pre_confirmedCount"])
        pre_confirmedIncr_list.append(data_list[i]["pre_confirmedIncr"])
    return time_list, confirmedCount_list, confirmedIncr_list, pre_confirmedCount_list, pre_confirmedIncr_list


# 将请求定位到predict_index.html文件中
def get_predict_inedx(request):
    return render(request,'predict/predict_index.html')

def get_simulation_result(request):
    pop = request.GET.get('pop')
    beta = request.GET.get('beta')
    gamma = request.GET.get('gamma')
    lambd = request.GET.get('lambd')
    omega = request.GET.get('omega')
    kappa = request.GET.get('kappa')
    model = request.GET.get('model')
    if(model == 'SIR模型'):
        incr = SIR_model(int(pop),float(beta),float(gamma))[0]
    elif(model == 'SEIR模型'):
        incr = SEIR_model(int(pop), float(beta), float(lambd), float(gamma))[0]
    elif (model == 'RLIM模型'):
        incr = RMIL_model(int(pop), float(beta), float(lambd), float(gamma), float(kappa), float(omega))[0]
    #accu = SIR_model(int(pop),float(beta),float(gamma))[1]
    # return render(request,'predict/predict_index.html',{
    #                 'incr': json.dumps(incr),
    #                 'accu': json.dumps(accu),
    #                 })
    #res = zip(incr,accu)
    res = {'incr': incr}
    return HttpResponse(json.dumps(res))


#日期转换为字符串
def replace_date(dt):
    temp = dt.strftime("%Y-%m-%d")
    date = str(temp)
    return date

#替换中文
def replace_chinese(str):
    name = {
        "Afghanistan": "阿富汗",
        "Andorra" : "安道尔",
        "Angola": "安哥拉",
        "Antigua and Barbuda" : "安提瓜和巴布达",
        "Albania": "阿尔巴尼亚",
        "Algeria": "阿尔及利亚",
        "Argentina": "阿根廷",
        "Armenia": "亚美尼亚",
        "Australia": "澳大利亚",
        "Austria": "奥地利",
        "Azerbaijan": "阿塞拜疆",
        "Bahamas": "巴哈马",
        "Bahrain" : "巴林",
        "Bangladesh": "孟加拉国",
        "Barbados": "巴巴多斯",
        "Belgium": "比利时",
        "Benin": "贝宁",
        "Burkina Faso": "布基纳法索",
        "Burundi": "布隆迪",
        "Bulgaria": "保加利亚",
        "Bosnia and Herz.": "波斯尼亚和黑塞哥维那",
        "Bosnia and Herzegovina":"波斯尼亚和黑塞哥维那",
        "Belarus": "白俄罗斯",
        "Belize": "伯利兹",
        "Bermuda": "百慕大群岛",
        "Bolivia": "玻利维亚",
        "Brazil": "巴西",
        "Brunei": "文莱",
        "Bhutan": "不丹",
        "Botswana": "博茨瓦纳",
        "Cambodia": "柬埔寨",
        "Cameroon": "喀麦隆",
        "Canada": "加拿大",
        "Cayman Islands" : "开曼群岛",
        "Cape Verde": "佛得角共和国",
        "Central African Rep.": "中非共和国",
        "Central African Republic": "中非共和国",
        "Chad": "乍得",
        "Chile": "智利",
        "China": "中国",
        "Colombia": "哥伦比亚",
        "Comoros": "科摩罗",
        "Congo": "刚果",
        "Costa Rica": "哥斯达黎加",
        "CÃ´te d'Ivoire": "科特迪瓦",
        "Croatia": "克罗地亚",
        "Cuba": "古巴",
        "Cyprus": "塞浦路斯",
        "Czech Rep.": "捷克共和国",
        "Dem. Rep. Korea": "韩国",
        "Dem. Rep. Congo": "民主刚果",
        "Democratic Republic of Congo": "民主刚果",
        "Democratic Republic " : "民主刚果",
        "Denmark": "丹麦",
        "Djibouti": "吉布提",
        "Dominica": "多米尼克",
        "Dominican Rep.": "多米尼加共和国",
        "Dominican Republic" : "多米尼加共和国",
        "Ecuador": "厄瓜多尔",
        "Egypt": "埃及",
        "El Salvador": "萨尔瓦多",
        "Eq. Guinea": "赤道几内亚",
        "Equatorial Guinea" :"赤道几内亚",
        "Eritrea": "厄立特里亚",
        "Estonia": "爱沙尼亚",
        "Eswatini": "斯威士兰",
        "Ethiopia": "埃塞俄比亚",
        "Falkland Is.": "福克兰群岛",
        "Falkland Islands": "福克兰群岛",
        "Faeroe Islands": "法罗群岛",
        "Fiji": "斐济",
        "Finland": "芬兰",
        "France": "法国",
        "French Guiana": "法属圭亚那",
        "Fr. S. Antarctic Lands": "法属南部领地",
        "Gabon": "加蓬",
        "Gambia": "冈比亚",
        "Germany": "德国",
        "Georgia": "佐治亚州",
        "Ghana": "加纳",
        "Gibraltar":"直布罗陀",
        "Greece": "希腊",
        "Greenland": "格陵兰",
        "Grenada": "格林纳达",
        "Guatemala": "危地马拉",
        "Guernsey": "根西",
        "Guinea": "几内亚",
        "Guinea-Bissau": "几内亚比绍",
        "Guyana": "圭亚那",
        "Haiti": "海地",
        "Heard I. and McDonald Is.": "赫德岛和麦克唐纳群岛",
        "Honduras": "洪都拉斯",
        "Hong Kong": "香港",
        "Hungary": "匈牙利",
        "Iceland": "冰岛",
        "India": "印度",
        "Indonesia": "印度尼西亚",
        "Iran": "伊朗",
        "Iraq": "伊拉克",
        "Ireland": "爱尔兰",
        "Isle of Man": "马恩岛",
        "Israel": "以色列",
        "Italy": "意大利",
        "Ivory Coast": "象牙海岸",
        "Jamaica": "牙买加",
        "Japan": "日本",
        "Jersey": "泽西岛",
        "Jordan": "乔丹",
        "Kashmir": "克什米尔",
        "Kazakhstan": "哈萨克斯坦",
        "Kenya": "肯尼亚",
        "Kosovo": "科索沃",
        "Kuwait": "科威特",
        "Kyrgyzstan": "吉尔吉斯斯坦",
        "Laos": "老挝",
        "Lao PDR": "老挝人民民主共和国",
        "Latvia": "拉脱维亚",
        "Lebanon": "黎巴嫩",
        "Lesotho": "莱索托",
        "Liberia": "利比里亚",
        "Libya": "利比亚",
        "Liechtenstein": "列支敦士登",
        "Lithuania": "立陶宛",
        "Luxembourg": "卢森堡",
        "Madagascar": "马达加斯加",
        "Macedonia": "马其顿",
        "Macao":"澳门",
        "Malawi": "马拉维",
        "Maldives": "马尔代夫共和国",
        "Malaysia": "马来西亚",
        "Mali": "马里",
        "Malta":"马耳他共和国",
        "Mauritius": "毛里求斯",
        "Marshall Islands":"马绍尔群岛",
        "Mauritania": "毛里塔尼亚",
        "Mexico": "墨西哥",
        "Micronesia (country)": "密克罗尼西亚联邦",
        "Moldova": "摩尔多瓦",
        "Monaco": "摩纳哥",
        "Mongolia": "蒙古",
        "Montenegro": "黑山",
        "Morocco": "摩洛哥",
        "Mozambique": "莫桑比克",
        "Myanmar": "缅甸",
        "Namibia": "纳米比亚",
        "Netherlands": "荷兰",
        "New Caledonia": "新喀里多尼亚",
        "New Zealand": "新西兰",
        "Nepal": "尼泊尔",
        "Nicaragua": "尼加拉瓜",
        "Niger": "尼日尔",
        "Nigeria": "尼日利亚",
        "Korea": "朝鲜",
        "Northern Cyprus": "北塞浦路斯",
        "Norway": "挪威",
        "Oman": "阿曼",
        "Palestine": "巴勒斯坦",
        "Pakistan": "巴基斯坦",
        "Panama": "巴拿马",
        "Papua New Guinea": "巴布亚新几内亚",
        "Paraguay": "巴拉圭",
        "Peru": "秘鲁",
        "Republic of the Congo": "刚果共和国",
        "Philippines": "菲律宾",
        "Poland": "波兰",
        "Portugal": "葡萄牙",
        "Puerto Rico": "波多黎各",
        "Qatar": "卡塔尔",
        "Republic of Seychelles": "塞舌尔共和国",
        "Romania": "罗马尼亚",
        "Russia": "俄罗斯",
        "Rwanda": "卢旺达",
        "Saint Lucia": "圣卢西亚",
        "Saint Vincent and th": "圣文森特和格林纳丁斯",
        "Saint Vincent and the Grenadines": "圣文森特和格林纳丁斯",
        "Saint Kitts and Nevi": "圣基茨和尼维斯联邦",
        "Saint Kitts and Nevis": "圣基茨和尼维斯联邦",
        "Samoa": "萨摩亚",
        "San Marino": "圣马力诺共和国",
        "Sao Tome and Princip": "圣多美和普林西比",
        "Sao Tome and Principe": "圣多美和普林西比",
        "Saudi Arabia": "沙特阿拉伯",
        "Senegal": "塞内加尔",
        "Serbia": "塞尔维亚",
        "Seychelles": "塞舌尔",
        "Sierra Leone": "塞拉利昂",
        "Singapore" : "新加坡",
        "Slovakia": "斯洛伐克",
        "Slovenia": "斯洛文尼亚",
        "Solomon Is.": "所罗门群岛",
        "Solomon Islands": "所罗门群岛",
        "Somaliland": "索马里兰",
        "Somalia": "索马里",
        "South Africa": "南非",
        "S. Geo. and S. Sandw. Is.": "南乔治亚和南桑德威奇群岛",
        "S. Sudan": "南苏丹",
        "Spain": "西班牙",
        "Sri Lanka": "斯里兰卡",
        "Sudan": "苏丹",
        "Suriname": "苏里南",
        "Swaziland": "斯威士兰",
        "Sweden": "瑞典",
        "Switzerland": "瑞士",
        "Syria": "叙利亚",
        "Tajikistan": "塔吉克斯坦",
        "Taiwan": "台湾",
        "Tanzania": "坦桑尼亚",
        "Thailand": "泰国",
        "The Kingdom of Tonga": "汤加王国",
        "Timor-Leste": "东帝汶",
        "Timor": "东帝汶",
        "Togo": "多哥",
        "Trinidad and Tobago": "特立尼达和多巴哥",
        "Tunisia": "突尼斯",
        "Turkey": "土耳其",
        "Turks and Caicos Islands": "特克斯和凯科斯群岛",
        # "Turkmenistan": "土库曼斯坦",
        "Uganda": "乌干达",
        "Ukraine": "乌克兰",
        "United Arab Emirates": "阿拉伯联合酋长国",
        "United Kingdom": "英国",
        "United Republic of Tanzania": "坦桑尼亚联合共和国",
        "United States": "美国",
        "United States of America": "美利坚合众国",
        "Uruguay": "乌拉圭",
        "Uzbekistan": "乌兹别克斯坦",
        "Vatican" : "梵蒂冈",
        "Vanuatu": "瓦努阿图",
        "Venezuela": "委内瑞拉",
        "Vietnam": "越南",
        "West Bank": "西岸",
        "W. Sahara": "西撒哈拉",
        "Yemen": "也门",
        "Zambia": "赞比亚",
        "Zimbabwe": "津巴布韦"
    }
    if name[str]:
        chinesename = name[str]
    else:
        chinesename = str
    return chinesename





