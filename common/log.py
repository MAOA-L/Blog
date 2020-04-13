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
        self.has_log = {}

    def _out(self, level="INFO", msg=None):
        getattr(self.log, level.lower())(msg)

    def info(self, msg):
        self._out(level="info", msg=msg)

    def error(self, msg):
        self._out(level="error", msg=msg)

    def get_logger(self, log_name):
        _log = self.has_log.get(log_name)
        if not _log:
            _log = logging.getLogger(log_name)
            self.has_log[log_name] = _log
            return _log


log_common = Log()
