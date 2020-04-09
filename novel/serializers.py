# -*- coding: utf-8 -*-
"""
 @Time    : 2020/4/10 0:14
 @Author  : CyanZoy
 @File    : serializers.py
 @Software: PyCharm
 @Describe: 
 """
from rest_framework import serializers

from novel.models import GraspRule


class CreateGraspRuleSerializer(serializers.ModelSerializer):
    """创建抓取规则序列化器"""

    class Meta:
        model = GraspRule
        fields = (
            'service',
            'host',
            'section_rule',
            'content_rule',
        )