# -*- coding: utf-8 -*-
"""
 @Time    : 2018/11/14 20:43
 @Author  : CyanZoy
 @File    : urls.py
 @Software: PyCharm
 """
from django.conf import urls
from django.conf.urls import url
from django.urls import path
from bus import views as bus_views

urlpatterns = [
    # describe: 初始化数据
    # 初始化公交基本信息
    url(r'^initBusBaseInfo/$', bus_views.InitBusBaseInfo.as_view()),
    # 初始化公交实况链接
    url(r'^InitBusRealUrl/$', bus_views.InitBusRealUrl.as_view()),

    # 获取公交基础信息
    url(r'^getBusInfo/$', bus_views.GetBusInfo.as_view()),
    # 获取公交的实况信息
    url(r'^getBusRealTimeInfo/$', bus_views.GetBusRealTimeInfo.as_view()),



    url(r'^testViewToSocket/$', bus_views.TestViewToSocket.as_view()),


]
