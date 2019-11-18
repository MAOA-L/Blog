# -*- coding: utf-8 -*-
"""
 @Time    : 2018/4/22 16:59
 @Author  : CyanZoy
 @File    : test.py
 @Software: PyCharm
 """
import re

str = 'http://pic1.win4000.com/mobile/3/573e6f8a50eb8.jpg'
f = re.findall('(.*com)', str)
g = re.findall('[a-zA-Z0-9].*', re.findall('com(.*)', str)[0])
k = re.findall('http:.*\.com', str)
print(k)
print(g)

s = ''.join(k+['/']+g)

print(s)