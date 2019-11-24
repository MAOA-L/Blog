# -*- coding: utf-8 -*-
"""
 @Time    : 19/11/24 15:55
 @Author  : CyanZoy
 @File    : serializers.py
 @Software: PyCharm
 @Describe: 
 """
from rest_framework import serializers

from Bus.models import BusInfo


class GetBusStationsSerializer(serializers.ModelSerializer):
    """
    获取公交基本信息
    """

    number = serializers.SerializerMethodField(label="路号")

    def get_number(self, obj):
        return obj.number[:obj.number.find("路")+1] if obj.number.find("路") else obj.number

    class Meta:
        model = BusInfo
        fields = (
            'id',
            'number',
            'departure_station',
            'destination',
            'code',
            'bus_type',
        )