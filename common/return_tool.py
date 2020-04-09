# -*- coding: utf-8 -*-
"""
 @Time    : 2020/4/10 0:25
 @Author  : CyanZoy
 @File    : return_tool.py
 @Software: PyCharm
 @Describe: 
 """
from django.http import JsonResponse
from rest_framework import status


class SuccessHR(JsonResponse):
    def __init__(self, data=None, errmsg="请求成功", errcode=0, status_code=0):
        super().__init__({'errmsg': errmsg, 'errcode': errcode, 'status_code': status_code, 'data': data},
                         json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)