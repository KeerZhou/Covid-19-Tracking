from django.db import models
#定义应用模型
# Create your models here.

class Article(models.Model):
    article_id = models.AutoField(primary_key = True)
    title = models.CharField('标题', max_length=255)
    author = models.CharField('作者', max_length=255)
    url = models.CharField('文章链接', max_length=500)
    source = models.CharField('文章来源', max_length=500)
    source_url = models.CharField('文章来源链接', max_length=500)
    content = models.CharField('内容', max_length=500)
    publish_date = models.DateTimeField('发布日期', max_length=20)

class News(models.Model):
    news_id = models.AutoField(primary_key = True)
    news_title = models.CharField('新闻标题', max_length=255)
    news_url = models.CharField('新闻链接', max_length=500)
    source = models.CharField('新闻来源', max_length=500)
    source_url = models.CharField('新闻来源链接', max_length=500)
    news_content = models.CharField('新闻内容', max_length=2000)
    publish_date = models.DateTimeField('发布日期', max_length=20)
    news_photo_index = models.CharField('新闻图片', max_length=255)

class Research(models.Model):
    research_id = models.AutoField(primary_key = True)
    research_title = models.CharField('研究标题', max_length=255)
    research_url = models.CharField('新闻链接', max_length=500)
    author = models.CharField('作者', max_length=255)
    source = models.CharField('出版杂志', max_length=255)
    source_url = models.CharField('出版杂志链接', max_length=500)
    publish_date = models.DateTimeField('发布日期', max_length=20)

class Predict_result(models.Model):
    predict_result_id = models.AutoField(primary_key = True)
    countryName = models.CharField('国家名字', max_length=255)
    cityName =  models.CharField('城市名字', max_length=255)
    date = models.DateTimeField('日期', max_length=20)
    confirmedCount = models.IntegerField('累计确诊', max_length=11)
    confirmedIncr = models.IntegerField('新增确诊', max_length=11)
    pre_confirmedCount = models.IntegerField('预测累计确诊', max_length=11)
    pre_confirmedIncr = models.IntegerField('预测新增确诊', max_length=11)
    omega = models.FloatField('复阳率', max_length=11)
    predict_photo_index = models.CharField('预测图片', max_length=255)


class Confirmed_data(models.Model):
    countryName = models.CharField('国家名字', max_length=20)
    countryFullName = models.CharField('国家全名', max_length=20)
    date = models.DateTimeField('日期', max_length=20)
    confirmedCount = models.IntegerField('累计确诊', max_length=11)
    confirmedIncr = models.IntegerField('新增确诊', max_length=11)
    curedCount = models.IntegerField('累计治愈', max_length=11)
    curedIncr = models.IntegerField('新增治愈', max_length=11)
    currentConfirmedCount = models.IntegerField('当前累计确诊', max_length=11)
    currentConfirmedIncr = models.IntegerField('当前新增确诊', max_length=11)
    deadCount = models.IntegerField('累计死亡', max_length=11)
    deadIncr = models.IntegerField('新增死亡', max_length=11)
    suspectedCount = models.IntegerField('疑似确诊', max_length=11)
    suspectedCountIncr = models.IntegerField('疑似新增确诊', max_length=11)
