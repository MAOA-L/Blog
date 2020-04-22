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

    # number = serializers.SerializerMethodField(label="路号")
    mark = serializers.SerializerMethodField(label="备注")

    def get_mark(self, obj):
        # 获取站点信息
        bus_stations_name = BusStations.objects.filter(is_active=True, bus=obj).values("name")
        return ",".join([i['name'] for i in bus_stations_name])

    # def get_number(self, obj):
    #     return obj.number[:obj.number.find("路") + 1] if obj.number.find("路") else obj.number

    class Meta:
        model = BusInfo
        fields = (
            'id',
            'number',
            'departure_station',
            'destination',
            'code',
            'bus_type',
            'mark',
        )


class GetBusStationsSerializer(serializers.ModelSerializer):
    """获取站点信息"""

    status = serializers.SerializerMethodField(label="站点状态")

    def get_status(self, obj: BusStations):
        # 0行驶中 1到站 离站
        real_info = self.context.get("real_info", None)
        if not real_info:
            return -1
        else:
            if obj.station_id in real_info.keys():
                return int(real_info[obj.station_id].get("yxbj"))
        return -1

    class Meta:
        model = BusStations
        fields = (
            'id',
            'name',
            'station_id',
            'status',
        )
