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
    url(r'^getBusStations/$', bus_views.GetBusStations.as_view()),
    # 初始化公交基本信息
    url(r'^initBusBaseInfo/$', bus_views.InitBusBaseInfo.as_view())
]
