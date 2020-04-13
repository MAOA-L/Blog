import json
import logging
import time
import uuid
from urllib import parse

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from common.log import log_common


class TimeLogMiddleware(MiddlewareMixin):
    """
    请求时间统计
    """

    def process_request(self, request):
        request.REQUEST_TIME = time.time()

    def process_response(self, request, response):
        time_logger = log_common.get_logger("time.request")
        ip = request.META.get('REMOTE_ADDR', 'NO IP')
        msg = "{0}\t{1}\t{2}".format(ip, request.path, str((time.time() - request.REQUEST_TIME) * 1000))
        time_logger.info(msg)
        return response
