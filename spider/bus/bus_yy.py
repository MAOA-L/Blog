# -*- coding: utf-8 -*-
"""
 @Time    : 2018/11/14 20:48
 @Author  : CyanZoy
 @File    : bus_yy.py
 @Software: PyCharm
 @describe: 爬虫-余姚公交车列表
 """
from spider.bus import info
import requests
from lxml import etree
import random
import re
from collections import defaultdict
import base64


def search_list(number=''):
    """
    :param number: bus number，'' is default value
    :return: [['name', 'addresss'],[],……]
    """
    html = requests.get(url=info.url_search.format(number),
                        headers={'User-Agent': info.User_Agent[random.randint(0, 99) % 2]}).content.decode('utf-8')
    parse_html = etree.HTML(html)
    bus_list = parse_html.xpath(info.rule_bus_list)
    return [[w.text, w.xpath('./@href')] for w in sorted(bus_list, key=lambda k: k.text)]


def get_bus_station(bus_url=''):
    """
    :param bus_url: 具体车辆的url
    :return:
    :describe: 根据具体车辆url获取实况url再获取站点信息，ajax，返程url
    """
    if bus_url == '':
        return None
    if 'gpsbus.php' in bus_url:
        # print('bus_url', bus_url)
        return get_bus_live(bus_url)
    if 'http' not in bus_url:
        bus_url = info.service + bus_url
    results = defaultdict(list)
    html = requests.get(url=bus_url, headers={'User-Agent': info.User_Agent[random.randint(0, 99) % 2]}).content.decode(
        'utf-8')
    parse_html = etree.HTML(html)
    try:
        bus_live = parse_html.xpath('//div[@class="subNav"]/a/@href')[0]
        results['bus_live'] = bus_live
        get_bus_live(bus_live, results)
        return results
    except Exception:
        pass


def get_bus_live(bus_live, results=None):
    if results is None:
        results = defaultdict(list)
    html2 = requests.get(url=bus_live,
                         headers={'User-Agent': info.User_Agent[random.randint(0, 99) % 2]}).content.decode('utf-8')
    data = re.search('data: "(.*)"', html2).group(1)
    results['ajax'] = data
    parse_html2 = etree.HTML(html2)
    bus_stations = parse_html2.xpath('//ul[@id="touchBox"]/li')
    for i in bus_stations:
        results['bus_stations'].append([i.text, i.get('id')])
    bus_number = parse_html2.xpath('//div[@class="subNav"]/strong')[0]
    results['bus_number'] = bus_number
    bus_back = parse_html2.xpath('//div[@class="subNav"]/a/@href')[0]
    results['bus_back'] = bus_back
    return results


def gei_ajax_info(ajax_url=''):
    import json
    if ajax_url is None or ajax_url == '':
        return None
    json_ajax = requests.get(url=info.getGpsInfoCs + '?' + ajax_url,
                             headers={'User-Agent': info.User_Agent[random.randint(0, 99) % 2]}).content.decode('utf-8')
    json_ajax = json.loads(json_ajax)
    return json_ajax
    # for i in json_ajax:
    #     print(i)
