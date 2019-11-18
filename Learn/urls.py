# -*- coding: utf-8 -*-
"""
 @Time    : 2018/7/30 19:52
 @Author  : CyanZoy
 @File    : urls.py
 @Describe:
 """
from django.urls import path
from .views import *

urlpatterns = [
    path('', index)
]
