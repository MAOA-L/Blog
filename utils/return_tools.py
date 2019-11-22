# from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework import status


def success_hr(data=None, errmsg="请求成功", errcode=0, status_code=0):
    return JsonResponse({'errmsg': errmsg, 'errcode': errcode, 'status_code': status_code, 'data': data},
                        json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)


def error_hr(data=None, errmsg="请求失败", errcode=1, status_code=1):
    return JsonResponse({'errmsg': errmsg, 'errcode': errcode, 'status_code': status_code, 'data': data},
                        json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)
