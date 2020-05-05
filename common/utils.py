# -*- coding: utf-8 -*-
"""
 @Time    : 2020/4/10 0:18
 @Author  : CyanZoy
 @File    : utils.py
 @Software: PyCharm
 @Describe: 
 """
import requests
from lxml import etree

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
}


# 发送请求
def requests_get(url, headers=None, decode='utf-8', j=False):
    if not headers:
        headers = HEADERS
    res = requests.get(url=url, headers=headers, verify=False)
    if j:
        return res.json()
    return res.content.decode(decode)


# 解析网页
def html_to_etree(html_raw):
    return etree.HTML(html_raw)
