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
from Bus import views as bus_views

urlpatterns = [
    # path('index', views.index),
    # path('bus_search', views.bus_search),
    # path('', views.index),
    url(r'^bus/getBusStations/$', bus_views.GetBusStations.as_view())
]
