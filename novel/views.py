from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics

from base.views import BaseAPIView
from common.return_tool import SuccessHR, ErrorHR
from common.utils import requests_get, html_to_etree
from novel.models import GraspRule, NovelEntry, NovelSection
from novel.serializers import CreateGraspRuleSerializer


class CreateNovelEntry(BaseAPIView, generics.CreateAPIView):
    pass


class CreateGraspRule(BaseAPIView, generics.CreateAPIView):
    """创建抓取规则"""
    serializer_class = CreateGraspRuleSerializer


class GetNovelSections(BaseAPIView, generics.ListAPIView):
    """抓取小说的主体信息和章节信息"""

    def list(self, request, *args, **kwargs):
        host = request.query_params.get("host")
        url = request.query_params.get("url")
        book_name = request.query_params.get("book_name")
        if not url:
            return ErrorHR("参数url缺失")
        if host:
            self.query_sql &= Q(host__contains=host)
        book = self.get_novel_entry(book_name=book_name)
        if not book:
            return ErrorHR("不存在该书")
        # 获取章节的抓取规则
        rule = GraspRule.objects.filter(self.query_sql).first()
        list_rule = rule.list_rule
        section_rule_p = rule.section_rule_p
        section_rule = rule.section_rule

        res = requests_get(url=url, decode='gbk')
        parse_html = html_to_etree(res)
        sections = []
        # 获取章节列表
        section_p = parse_html.xpath(list_rule)
        section_p_obj = None
        need_add_obj = []
        for i in section_p:
            # 判断是否为父级目录
            if dict(i.attrib).get("class") == section_rule_p:
                # 判断need_add_obj 有就新增
                if need_add_obj:
                    NovelSection.objects.bulk_create(need_add_obj)
                    need_add_obj.clear()
                _name = i.text
                section_p_obj = self.create_section(novel=book, name=_name)
            else:
                # 获取目录
                a = i.xpath(section_rule)
                if a:
                    o = a[0]
                    href = o.xpath("./@href")[0]
                    sec_name = o.text
                    need_add_obj.append(NovelSection(novel=book, name=sec_name, url=href, parent=section_p_obj))
        # 结束后再次判断need_add_obj
        if need_add_obj:
            NovelSection.objects.bulk_create(need_add_obj)
        return SuccessHR("创建成功")

    def get_novel_entry(self, book_name):
        """获取书本对象"""
        return NovelEntry.objects.filter(is_active=True, name=book_name).first()

    def create_section(self, novel, name, url=None, parent=None):
        """创建小说章节"""
        return NovelSection.objects.create(novel=novel, name=name, url=url, parent=parent)
