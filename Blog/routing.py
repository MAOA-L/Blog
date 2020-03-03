# -*- coding: utf-8 -*-
"""
 @Time    : 20/3/3 10:38
 @Author  : CyanZoy
 @File    : routing.py
 @Software: PyCharm
 @Describe: 
 """
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r'chat/', )
        ])
    )
})
