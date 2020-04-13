from collections import OrderedDict

from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from common.return_tool import SuccessHR


class CustomPagination(PageNumberPagination):
    page_size = 10

    page_query_param = "pageNo"
    page_size_query_param = 'pageSize'

    def get_paginated_response(self, data):

        if hasattr(self, 'page'):
            content = OrderedDict([
                ('pageNo', self.page.number),
                ('pageSize', self.page.paginator.per_page),
                ('total', self.page.paginator.count),
                # ('next', self.get_next_link()),
                # ('previous', self.get_previous_link()),
                ('list', data)
            ])
        else:
            # TODO self.page 属性不存在， 下述字段值需要重新获取
            content = OrderedDict([
                ('pageNo', 0),
                ('pageSize', self.page_size),
                ('total', 0),
                # ('next', self.get_next_link()),
                # ('previous', self.get_previous_link()),
                ('list', [])
            ])

        return SuccessHR(content)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        try:
            page = super().paginate_queryset(queryset, request, view)
            return page
        except NotFound:
            return []
