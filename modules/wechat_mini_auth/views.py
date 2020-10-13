import requests
from django.shortcuts import render
from rest_framework import generics

from base.views import BaseAPIView
from common.return_tool import SuccessHR


def get_code2session(jscode):
    secret = "7dda30274be67de36f841c01d63ad8ff"
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={jscode}&grant_type=authorization_code"
    url_fmt = url.format(appid="wx0fad17ea213e7298", secret=secret, jscode=jscode)
    rsp = requests.get(url=url_fmt)
    print(rsp.json())


def get_user_info():
    """"""


class WechatLogin(BaseAPIView, generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        code = request.query_params.get("code")
        print(code)
        get_code2session(jscode=code)

        return SuccessHR({
            "name": "success"
        })
