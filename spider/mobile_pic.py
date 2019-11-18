# -*- coding: utf-8 -*-
"""
 @Time    : 2018/7/19 11:03
 @Author  : CyanZoy
 @File    : mobile_pic.py
 @Software: PyCharm
 """
import requests
import random
from lxml import etree
import re


class F:
    def __init__(self):
        self.url = 'http://www.win4000.com/mobile_2344_0_0_{}.html'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'}

    def get_image_url(self):
        try:
            html = requests.get(url=self.url.format(random.randint(1, 5)), headers=self.headers).content.decode('utf-8')
            html = etree.HTML(html)
            a = html.xpath('//ul[@class="clearfix"]')
            a = a[1].xpath('./li/a/@href')
            # 随机抽取a中的href获取大图url
            ll = requests.get(url=a[random.randint(0, len(a))], headers=self.headers).content.decode('utf-8')
            ll = etree.HTML(ll)
            pic_large = ll.xpath('//img[@class="pic-large"]/@src')
            g = re.findall('[a-zA-Z0-9].*', re.findall('com(.*)', pic_large[0])[0])
            k = re.findall('http:.*\.com', pic_large[0])
            return ''.join(k+['/']+g)
        except Exception as e:
            pass


if __name__ == "__main__":
    print(F().get_image_url())