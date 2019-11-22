# -*- coding: utf-8 -*-
"""
 @Time    : 19/11/22 15:53
 @Author  : CyanZoy
 @File    : http_requests.py
 @Software: PyCharm
 @Describe: 
 """
import json
import os

import django
import requests
from lxml.html import html_parser

from spider.bus.info import User_Agent
from lxml import etree

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Blog.settings")
django.setup()
from Bus.models import BusInfo


def fetch_html(url, method="GET", data=None, headers=None, charset='gbk'):
    """
    :param url:
    :param method:
    :param data:
    :param headers:
    :param charset:
    :return:
    """
    if not headers:
        headers = {
            "User_Agent": User_Agent,
        }

    assert method in ['GET', "POST"]
    content = None
    if method.lower() == "get":
        content = requests.get(url=url, headers=headers).content.decode(charset).encode("utf-8").decode("utf-8")
    if method.lower() == "post":
        content = requests.post(url=url, params=data, headers=headers).content.decode(charset)
    return content


def recursion(element):
    """递归解析元素 本规则只适用于此类型页面http://bm.eyuyao.com/bus/type/ChengQuGongJiao.html"""
    p = []
    if hasattr(element, 'getchildren') and element.getchildren():
        if element.tag == 'table' and element.attrib['width'] not in ['850', '815']:
            return
        if element.getchildren()[0].tag == 'br' and element.text:
            p.append(element.text)
        for i in element.getchildren():
            # 进行递归解析
            tem = recursion(i)
            if tem:
                p.append(tem)
    else:
        # 没有子元素, 开始解析
        if element.tag == 'a':
            return element.xpath("./@href"), element.text
        if element.tag == 'td':
            text = element.text
            if text:
                return text.replace("\xa0", "")
            else:
                return text
        if element.tag == 'span':
            return element.text
        if element.tag == 'b':
            return element.text
    return p if p else None


if __name__ == '__main__':
    url = 'http://bm.eyuyao.com/bus/type/ChengQuGongJiao.html'
    # url = 'https://www.cyanzoy.top/post/LfH2aK5oT/'
    content = fetch_html(url=url)
    if content:
        content = etree.HTML(content)
        table_list = content.xpath("//table")
        p = {}
        count = 0
        for i, v in enumerate(table_list):
            con = recursion(v)
            if con:
                p[count] = con
                count += 1
        # print(json.dumps(p, ensure_ascii=False))
        bus_info_list = []
        for i in p[0][1]:
            for j in i:
                code, number = j
                *_, code = str(code[0]).rpartition("/")

                bus_info_list.append(BusInfo(
                    number=number,
                    code=code,
                    departure_station='',
                    destination=''
                ))
        BusInfo.objects.bulk_create(bus_info_list)
                # print(code, number)
