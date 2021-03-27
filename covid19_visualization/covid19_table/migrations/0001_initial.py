# Generated by Django 3.1.4 on 2021-03-18 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('article_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('author', models.CharField(max_length=255, verbose_name='作者')),
                ('url', models.CharField(max_length=500, verbose_name='文章链接')),
                ('source', models.CharField(max_length=500, verbose_name='文章来源')),
                ('source_url', models.CharField(max_length=500, verbose_name='文章来源链接')),
                ('content', models.CharField(max_length=500, verbose_name='内容')),
                ('publish_date', models.DateTimeField(max_length=20, verbose_name='发布日期')),
            ],
        ),
        migrations.CreateModel(
            name='Confirmed_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryName', models.CharField(max_length=20, verbose_name='国家名字')),
                ('countryFullName', models.CharField(max_length=20, verbose_name='国家全名')),
                ('date', models.DateTimeField(max_length=20, verbose_name='日期')),
                ('confirmedCount', models.IntegerField(max_length=11, verbose_name='累计确诊')),
                ('confirmedIncr', models.IntegerField(max_length=11, verbose_name='新增确诊')),
                ('curedCount', models.IntegerField(max_length=11, verbose_name='累计治愈')),
                ('curedIncr', models.IntegerField(max_length=11, verbose_name='新增治愈')),
                ('currentConfirmedCount', models.IntegerField(max_length=11, verbose_name='当前累计确诊')),
                ('currentConfirmedIncr', models.IntegerField(max_length=11, verbose_name='当前新增确诊')),
                ('deadCount', models.IntegerField(max_length=11, verbose_name='累计死亡')),
                ('deadIncr', models.IntegerField(max_length=11, verbose_name='新增死亡')),
                ('suspectedCount', models.IntegerField(max_length=11, verbose_name='疑似确诊')),
                ('suspectedCountIncr', models.IntegerField(max_length=11, verbose_name='疑似新增确诊')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('news_id', models.AutoField(primary_key=True, serialize=False)),
                ('news_title', models.CharField(max_length=255, verbose_name='新闻标题')),
                ('news_url', models.CharField(max_length=500, verbose_name='新闻链接')),
                ('source', models.CharField(max_length=500, verbose_name='新闻来源')),
                ('source_url', models.CharField(max_length=500, verbose_name='新闻来源链接')),
                ('news_content', models.CharField(max_length=2000, verbose_name='新闻内容')),
                ('publish_date', models.DateTimeField(max_length=20, verbose_name='发布日期')),
                ('news_photo_index', models.CharField(max_length=255, verbose_name='新闻图片')),
            ],
        ),
        migrations.CreateModel(
            name='Predict_result',
            fields=[
                ('predict_result_id', models.AutoField(primary_key=True, serialize=False)),
                ('countryName', models.CharField(max_length=255, verbose_name='国家名字')),
                ('cityName', models.CharField(max_length=255, verbose_name='城市名字')),
                ('date', models.DateTimeField(max_length=20, verbose_name='日期')),
                ('confirmedCount', models.IntegerField(max_length=11, verbose_name='累计确诊')),
                ('confirmedIncr', models.IntegerField(max_length=11, verbose_name='新增确诊')),
                ('pre_confirmedCount', models.IntegerField(max_length=11, verbose_name='预测累计确诊')),
                ('pre_confirmedIncr', models.IntegerField(max_length=11, verbose_name='预测新增确诊')),
                ('omega', models.FloatField(max_length=11, verbose_name='复阳率')),
                ('predict_photo_index', models.CharField(max_length=255, verbose_name='预测图片')),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('research_id', models.AutoField(primary_key=True, serialize=False)),
                ('research_title', models.CharField(max_length=255, verbose_name='研究标题')),
                ('research_url', models.CharField(max_length=500, verbose_name='新闻链接')),
                ('author', models.CharField(max_length=255, verbose_name='作者')),
                ('source', models.CharField(max_length=255, verbose_name='出版杂志')),
                ('source_url', models.CharField(max_length=500, verbose_name='出版杂志链接')),
                ('publish_date', models.DateTimeField(max_length=20, verbose_name='发布日期')),
            ],
        ),
    ]