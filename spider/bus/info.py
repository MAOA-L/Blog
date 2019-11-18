# -*- coding: utf-8 -*-
"""
 @Time    : 2018/11/14 21:04
 @Author  : CyanZoy
 @File    : info.py
 @Software: PyCharm
 """
# 服务器
service = 'http://bm.eyuyao.com/bus/mobile/'
# 发包信息
User_Agent = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36']
# 公交车搜索url 空白为默认全部
url_search = 'http://bm.eyuyao.com/bus/mobile/lineList.php?k=pp&q={}'
# ajax 不变部分
getGpsInfoCs = 'http://bm.eyuyao.com/bus/mobile/getGpsInfoCs.php'
# 解析规则
# 1.公交车列表信息
rule_bus_list = '//ul[@class="list borderNone mbNone"]/li/a'
