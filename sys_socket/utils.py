# -*- coding: utf-8 -*-
"""
 @Time    : 20/3/3 16:32
 @Author  : CyanZoy
 @File    : utils.py
 @Software: PyCharm
 @Describe: 
 """
from channels.db import database_sync_to_async

from Wx.models import Fund


@database_sync_to_async
def get_name(self):
    return Fund.objects.all()