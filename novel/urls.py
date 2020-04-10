# -*- coding: utf-8 -*-
"""
 @Time    : 2020/4/10 0:06
 @Author  : CyanZoy
 @File    : urls.py
 @Software: PyCharm
 @Describe: 
 """
from django.conf.urls import url

from novel import views

urlpatterns = [
    # describe: 抓取规则
    # 创建抓取规则
    url(r'^rule/createGraspRule/$', views.CreateGraspRule.as_view()),

    # 抓取小说的主体信息和章节信息
    url(r'^entry/getNovelSections/$', views.GetNovelSections.as_view()),
]