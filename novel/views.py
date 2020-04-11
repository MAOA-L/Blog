import os
from django.utils.http import urlquote
from collections import deque

from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import render
from rest_framework import generics

from Blog.settings import BASE_DIR
from base.views import BaseAPIView
from common.log import log_common
from common.return_tool import SuccessHR, ErrorHR
from common.utils import requests_get, html_to_etree
from novel.models import GraspRule, NovelEntry, NovelSection, SectionContent
from novel.serializers import CreateGraspRuleSerializer, GetNovelSectionsSerializer
from novel.utils import get_content


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
        decode = rule.decode

        res = requests_get(url=url, decode=decode)
        parse_html = html_to_etree(res)
        sections = []
        # 获取章节列表
        section_p = parse_html.xpath(list_rule)
        section_p_obj = None
        need_add_obj = []
        order = 0
        for i in section_p:
            # 判断是否为父级目录
            if dict(i.attrib).get("class") == section_rule_p and section_rule_p is not None:
                order = 0
                # 判断need_add_obj 有就新增
                if need_add_obj:
                    NovelSection.objects.bulk_create(need_add_obj)
                    need_add_obj.clear()
                _name = i.text
                section_p_obj = self.create_section(novel=book, name=_name)
            else:
                # 获取目录
                order += 1
                a = i.xpath(section_rule)
                if a:
                    o = a[0]
                    href = o.xpath("./@href")[0]
                    sec_name = o.text
                    need_add_obj.append(NovelSection(novel=book, name=sec_name,
                                                     url=href, parent=section_p_obj, order=order))
        # 结束后再次判断need_add_obj
        if need_add_obj:
            NovelSection.objects.bulk_create(need_add_obj)
        return SuccessHR("创建成功")

    def get_novel_entry(self, book_name):
        """获取书本对象"""
        return NovelEntry.objects.filter(is_active=True, name=book_name).first()

    def create_section(self, novel, name, url=None, parent=None, order=0):
        """创建小说章节"""
        return NovelSection.objects.create(novel=novel, name=name, url=url, parent=parent, order=order)


class GetNovelContent(BaseAPIView, generics.ListAPIView):
    """获取小说主体内容"""

    def list(self, request, *args, **kwargs):
        # 获取小说主体
        novel_id = request.query_params.get("novel_id")
        if not novel_id:
            return ErrorHR("请选择小说")
        try:
            novel = NovelEntry.objects.get(is_active=True, id=novel_id)
            host = novel.host
            url = novel.url
            # 获取抓取规则
            try:
                g_rule = GraspRule.objects.get(is_active=True, host=host, service=url)
            except GraspRule.DoesNotExist:
                return ErrorHR("不存在该小说的爬取规则配置")
            else:
                content_rule = g_rule.content_rule
                # 获取小说下未获取小说内容的章节
                # 获取已经爬取的章节
                exists_content = SectionContent.objects.filter(is_active=True, novel=novel)
                n_sections = NovelSection.objects.filter(is_active=True, novel=novel).exclude(
                    id__in=[i.id.hex for i in exists_content])
                # 生成格式
                n_sections_list = [i for i in GetNovelSectionsSerializer(n_sections, many=True).data]
                # 切片 100 个一组
                section_deque = deque(maxlen=100)
                for i in n_sections_list:
                    section_deque.append(i)
                    if len(section_deque) == 100:
                        # 获取章节的内容
                        result = get_content(sections=section_deque, host=host, content_rule=content_rule)
                        # 整理成对象
                        need_add_obj = []
                        for j in result:
                            pk = j.get("id")
                            content = j.get("content")
                            need_add_obj.append(SectionContent(
                                novel=novel,
                                section_id=pk,
                                content=content
                            ))
                        if need_add_obj:
                            SectionContent.objects.bulk_create(need_add_obj)
                        # 清空
                        log_common.out(msg="===清空队列===")
                        section_deque.clear()
                return SuccessHR("爬取成功")
        except NovelEntry.DoesNotExist:
            return SuccessHR("不存在该小说")
        except Exception as ex:
            print(ex)
            return SuccessHR("中断，可再次开启~")


class GetNovelToTxt(BaseAPIView, generics.RetrieveAPIView):
    """获取小说文本"""

    def retrieve(self, request, *args, **kwargs):
        # 获取小说主体
        novel_id = request.query_params.get("novel_id")
        try:
            novel = NovelEntry.objects.get(is_active=True, id=novel_id)
        except NovelEntry.DoesNotExist:
            return SuccessHR("不存在该小说")
        else:
            novel_name = novel.name
            # 判断是否已经存在该文件
            file_path = BASE_DIR + "/novel/" + novel_name + ".txt"
            if not os.path.exists(file_path):
                # 获取章节内容顺序
                sections = SectionContent.objects.filter(is_active=True, novel=novel).order_by("section__order")
                with open(file_path, "w+", encoding="utf-8") as f:
                    for i in sections:
                        log_common.out(msg=f"写入{i.section.name}")
                        f.write('\n' + i.section.name + '\n')
                        f.write(i.content)
                log_common.out(msg="写入完成")
            if os.path.exists(file_path):
                file = open(file_path, 'r', encoding="utf-8")
                response = self.get_file_response(file=file, file_name=novel_name + ".txt")
                return response

    def get_file_response(self, file, file_name):
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
        return response
