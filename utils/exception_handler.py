import logging
import traceback

from django.http import Http404, JsonResponse
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied, NotAuthenticated, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import set_rollback

from common.return_tool import ErrorHR


class BizException(Exception):
    default_detail = '系统错误'

    def __init__(self, detail=None):
        if detail is None:
            self.detail = self.default_detail
        else:
            self.detail = detail


class PermissionDeniedException(BizException):
    default_detail = '权限不足'


def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    traceback.print_exc()

    if isinstance(exc, PermissionDeniedException):
        permission_logger = logging.getLogger('permission_denied')
        permission_logger.error('path:{path}'.format(path=context['request'].path))
        permission_logger.exception(exc)

    else:
        request_logger = logging.getLogger('business_error')
        request_logger.error('path:{path}'.format(path=context['request'].path))
        request_logger.exception(exc)

    request_logger = logging.getLogger('django.request')
    request_logger.error('path:{path}'.format(path=context['request'].path))
    request_logger.exception(exc)

    set_rollback()

    if isinstance(exc, NotAuthenticated):
        return ErrorHR(data=None, status_code=401, errcode=1, msg="请登录")

    if isinstance(exc, exceptions.APIException):
        headers = {}
        # if getattr(exc, 'auth_header', None):
        #     headers['WWW-Authenticate'] = exc.auth_header
        # if getattr(exc, 'wait', None):
        #     headers['Retry-After'] = '%d' % exc.wait
        #
        # if isinstance(exc.detail, (list, dict)):
        #     data = exc.detail
        # else:
        #     data = {'detail': exc.detail}
        if isinstance(exc, (PermissionDenied, PermissionDeniedException)):
            return ErrorHR(data=None, status_code=403, errcode=1, msg="没有权限访问")

        elif isinstance(exc, MethodNotAllowed):
            return ErrorHR(data=None, status_code=405, errcode=1, msg=exc.detail)

        return ErrorHR(exc.detail)

    if isinstance(exc, (BizException,)):
        return ErrorHR(exc.detail)

    if isinstance(exc, Http404):
        return ErrorHR(data=None, status_code=404, errcode=1, msg="找不到资源")

    return ErrorHR('系统错误', )
