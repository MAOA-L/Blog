# -*- coding: utf-8 -*-
"""
 @Time    : 2018/11/14 20:43
 @Author  : CyanZoy
 @File    : urls.py
 @Software: PyCharm
 """
from django.conf import urls
from django.urls import path
from Bus import views

urlpatterns = [
    path('index', views.index),
    path('bus_search', views.bus_search),
    path('', views.index),
]
