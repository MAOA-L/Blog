"""
@Time     : 2020/10/12 11:33
@Author   : Czy
@Describe : 
"""
from django.conf.urls import url

from modules.wechat_mini_auth import views

urlpatterns = [
    url('^wechatLogin/$', views.WechatLogin.as_view())
]