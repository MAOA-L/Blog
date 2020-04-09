from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics

from base.views import BaseAPIView
from novel.models import GraspRule
from novel.serializers import CreateGraspRuleSerializer


class CreateGraspRule(BaseAPIView, generics.CreateAPIView):
    """创建抓取规则"""
    serializer_class = CreateGraspRuleSerializer


class GetNovelSections(BaseAPIView, generics.ListAPIView):
    """抓取小说的主体信息和章节信息"""

    def list(self, request, *args, **kwargs):
        host = request.query_params.get("host")
        if host:
            self.query_sql &= Q(host__contains=host)
        # 获取章节的抓取规则
        rule = GraspRule.objects.filter(self.query_sql).first()
        section_rule = rule.section_rule
        print(section_rule)
