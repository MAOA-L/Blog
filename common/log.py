# -*- coding: utf-8 -*-
"""
 @Time    : 2020/4/11 23:58
 @Author  : CyanZoy
 @File    : log.py
 @Software: PyCharm
 @Describe: 
 """
import logging


class Log:

    def __init__(self, log_name="console_print"):
        self.log = logging.getLogger(log_name)

    def out(self, level="INFO", msg=None):
        getattr(self.log, level.lower())(msg)


log_common = Log()
