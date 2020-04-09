from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics

from utils.pagination import CustomPagination
from utils.return_tools import success_hr


class BaseAPIView(generics.ListAPIView, generics.RetrieveAPIView):

    pagination_class = CustomPagination
    query_sql = Q(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_hr(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_hr(serializer.data)
