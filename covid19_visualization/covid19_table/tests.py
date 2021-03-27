# from django.test import TestCase
# #编写应用测试用例
# # Create your tests here.
#
# from django.shortcuts import render
# from django.shortcuts import  HttpResponse
# from covid19_table.models import Article
#
# import sys
# import os
# import django
#
# # 这两行很重要，用来寻找项目根目录，os.path.dirname要写多少个根据要运行的python文件到根目录的层数决定
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(BASE_DIR)
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covid19_visualization.settings')
# django.setup()
#
# from covid19_table.models import Confirmed_data
#
# if __name__ == '__main__':
#     confirmed_data = Confirmed_data.objects.raw(
#         "SELECT countryFullName,confirmedIncr FROM covid19_table_confirmed_data WHERE date like '2020-04-24%'")
#     countryname = confirmed_data[0]
#     confirmednum = confirmed_data[1]
#     confirmed_data_List = []
#     for i in range(0, len(confirmed_data)):
#         temp = {'name': countryname[i], 'value': confirmednum[i]}
#         confirmed_data_List.append(temp)
#     print(confirmed_data_List)
