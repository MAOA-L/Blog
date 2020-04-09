from django.db import models

from base.models import Base


class NovelEntry(Base):
    """小说信息"""
    name = models.CharField(verbose_name="小说名字", max_length=50)
    url = models.CharField(verbose_name="小说网站url", max_length=255)
    host = models.CharField(verbose_name="小说网站host", max_length=255)


class NovelSection(Base):
    """小说章节"""
    novel = models.ForeignKey(NovelEntry, verbose_name="小说", on_delete=models.SET_NULL)
    name = models.CharField(verbose_name="章节名", max_length=50)
    url = models.CharField(verbose_name="章节url", max_length=255)


class SectionContent(Base):
    """章节下的内容"""
    section = models.ForeignKey(NovelEntry, verbose_name="小说章节", on_delete=models.SET_NULL)
    content = models.TextField(verbose_name="章节下的主要内容")
