# -*- coding: utf-8 -*-
"""
 @Time    : 2018/3/17 13:12
 @Author  : CyanZoy
 @File    : Te.py
 @Describe: api接口签名验证
 """
import hashlib
import time
# appid 与 appsecret
APPID = '8947539b9ba847b2'
APPSECRET = '00d6c285b0b6d2fea8afe57a52120aa6'
# 参数
kahao = '20150114148'
name = 'aaa'
times = str(int(time.time()))

sortlist = [APPID, APPSECRET, kahao, name, times]
print(sortlist)
sha = hashlib.sha1()
sha.update(''.join(sortlist).encode('utf-8'))
print(sha.hexdigest())
