from django.urls import path, include

import covid19_table.views

urlpatterns = [
    path('hello_world', covid19_table.views.hellow_world),
    #path('index', covid19_table.views.index),
    path('index', covid19_table.views.get_confirmed_data),
    #path('content',covid19_table.views.article_content),
    path('predict',covid19_table.views.get_predict_inedx),
    path('simulation',covid19_table.views.get_simulation_result),
    path('assessment',covid19_table.views.get_assessment_inedx),
    path('assessment/detail/<cityName>',covid19_table.views.get_assessment_detail),
    path('changeomega',covid19_table.views.get_omega_result),
    path('research',covid19_table.views.get_research_page),
    path('news',covid19_table.views.get_news_page),
    path('article',covid19_table.views.get_inedx_page),
    path('article/detail/<int:article_id>',covid19_table.views.get_detail_page)
]