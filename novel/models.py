from django.db import models

from base.models import Base


class GraspRule(Base):
    """抓取规则"""
    service = models.CharField(verbose_name="网站服务地址", max_length=50, null=True)
    host = models.CharField(verbose_name="网站host", max_length=100)
    section_rule_p = models.CharField(verbose_name="父类章节抓取规则", max_length=100, null=True)
    section_rule = models.CharField(verbose_name="章节抓取规则", max_length=100)
    content_rule = models.CharField(verbose_name="内容抓取规则", max_length=100)


class NovelEntry(Base):
    """小说信息"""
    name = models.CharField(verbose_name="小说名字", max_length=50)
    url = models.CharField(verbose_name="小说网站url", max_length=255)
    host = models.CharField(verbose_name="小说网站host", max_length=255)


class NovelSection(Base):
    """小说章节"""
    novel = models.ForeignKey(NovelEntry, verbose_name="小说", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="章节名", max_length=50)
    url = models.CharField(verbose_name="章节url", max_length=255)
    parent = models.ForeignKey('self', verbose_name="章节再次分类", on_delete=models.CASCADE, null=True)


class SectionContent(Base):
    """章节下的内容"""
    section = models.ForeignKey(NovelEntry, verbose_name="小说章节", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="章节下的主要内容")
