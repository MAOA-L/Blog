# -*- coding: utf-8 -*-
"""
 @Time    : 19/11/24 15:55
 @Author  : CyanZoy
 @File    : serializers.py
 @Software: PyCharm
 @Describe: 
 """
from rest_framework import serializers

from bus.models import BusInfo, BusStations


class GetBusInfoSerializer(serializers.ModelSerializer):
    """
    获取公交基本信息
    """

    number = serializers.SerializerMethodField(label="路号")

    def get_number(self, obj):
        return obj.number[:obj.number.find("路") + 1] if obj.number.find("路") else obj.number

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


class GetBusStationsSerializer(serializers.ModelSerializer):
    """获取站点信息"""

    status = serializers.SerializerMethodField(label="站点状态")

    def get_status(self, obj):
        # 0行驶中 1到站 离站
        return 0

    class Meta:
        model = BusStations
        fields = (
            'id',
            'name',
            'station_id',
            'status',
        )
