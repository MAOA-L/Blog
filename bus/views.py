import datetime
import json
from collections import OrderedDict

from channels.layers import get_channel_layer
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from bus.models import BusInfo, BusStations
from bus.serializers import GetBusStationsSerializer, GetBusInfoSerializer
from base.views import BaseAPIView
from bus.utils import grab_base_bus, grab_bus_real_url, grab_bus_real_info, grab_real_info, grab_ajax_data
from spider.bus import bus_yy
from common.return_tool import SuccessHR, ErrorHR
from sys_socket.consumer import ViewSocket


def index(request):
    return render(request, 'htmls/bus_index.html')


def bus_search(request):
    from collections import defaultdict
    import base64
    import json
    if request.is_ajax():
        ajax_url = request.GET.get('ajax')
        # 将编码后接受的ajax去除&#39; （表示引号）和第一个b后解码，后用str()编码成utf-8
        parse_ajax = str(base64.b64decode(ajax_url.replace('&#39;', '')[1:]), 'utf-8')
        json_ajax = bus_yy.gei_ajax_info(parse_ajax)
        bus_live_info = []
        for _ in json_ajax:
            bus_live_info.append(_['nearstationid'])
        return HttpResponse(json.dumps(bus_live_info))
    puzzleid = request.GET.get('puzzleid')
    target = request.GET.get('target')
    bus_list = bus_yy.search_list()
    p = defaultdict(list)
    try:
        for i in bus_list:
            p[i[0][0]].append([i[0], i[1][0]])
    except Exception:
        pass
    if puzzleid:
        # 点击 1开头 则将1开头的车辆生成
        puzzle_bus = []
        for j in p[puzzleid]:
            puzzle_bus.append([j[0], str(base64.b64encode(str(j[1]).encode('utf-8')), "utf-8")])
        return render(request, 'htmls/bus_list.html', {'puzzle_bus': puzzle_bus})
    if target:
        results = bus_yy.get_bus_station(str(base64.b64decode(target), 'utf-8'))
        results['start_stations'] = '始发站:' + results['bus_stations'][0][0]
        results['bus_back'] = str(base64.b64encode(results['bus_back'].encode('utf-8')), "utf-8")
        results['ajax'] = base64.b64encode(results['ajax'].encode('utf-8'))
        return render(request, 'htmls/bus_list.html', results)

    return render(request, 'htmls/bus_list.html', {'bus_list': p})


class InitBusBaseInfo(BaseAPIView, generics.CreateAPIView):
    """初始化公交信息"""

    def post(self, request, *args, **kwargs):
        result = grab_base_bus()
        need_add_obj = []
        for i in result:
            name = i.get("name")
            href = i.get("href")
            need_add_obj.append(BusInfo(
                number=name,
                grab_real_url=href,
            ))
        BusInfo.objects.bulk_create(need_add_obj)
        return SuccessHR("初始化成功")


class InitBusRealUrl(BaseAPIView, generics.CreateAPIView):
    """初始化公交实况链接"""

    def post(self, request, *args, **kwargs):
        # 获取公交基础信息
        bus_info = BusInfo.objects.filter(is_active=True)
        bus_info_dict = [{"id": i.id.hex, "url": i.grab_real_url} for i in bus_info]
        result = grab_bus_real_url(bus_info_dict)
        raw = 0
        for i in result:
            pk = i.get("id")
            real_url = i.get("real_url")
            # 更新
            raw += BusInfo.objects.filter(is_active=True, id=pk).update(real_url=real_url)
        return SuccessHR({
            "data": result,
            "raw": raw
        })


class GetBusInfo(BaseAPIView, generics.ListAPIView):
    """
    获取公交基础信息列表
    """
    queryset = BusInfo.objects.filter().order_by('visit_traffic', 'order', 'bus_type', 'number', )
    serializer_class = GetBusInfoSerializer

    query_sql = Q(is_active=True)

    def get(self, request, *args, **kwargs):
        bus_type = self.request.query_params.get("t")  # 公交类型 uuid
        number = self.request.query_params.get("n")  # 公交线路名
        area = self.request.query_params.get("area_id", "城区")
        if area in [1, '1']:
            area = '城乡'
            self.query_sql &= Q(bus_type__name__contains=area)
        if bus_type:
            self.query_sql &= Q(bus_type__id=bus_type)
        if number:
            self.query_sql &= Q(number__contains=number)
        result_queryset = self.queryset.filter(self.query_sql)
        # result = OrderedDict()
        # for i in result_queryset:
        #     number = i.number[:i.number.find("路") + 1] if i.number.find("路") else i.number
        #     result.setdefault(number, GetBusInfoSerializer(i).data)

        # page = self.paginate_queryset(list(result.values()))
        page = self.paginate_queryset(result_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return SuccessHR(self.get_serializer(result_queryset.all(), many=True).data)


class GetBusRealTimeInfo(BaseAPIView, generics.ListAPIView):
    """
    获取实时信息
    策略:
        获取实况信息时,第一次会初始化公交站点的信息, 并做更新记录, 定时更新站点信息。
        此外直接获取实况信息与数据库数据进行匹配
    """

    def list(self, request, *args, **kwargs):
        pk = request.query_params.get("id")
        try:
            bus_info = BusInfo.objects.get(is_active=True, id=pk)
        except BusInfo.DoesNotExist:
            return ErrorHR("参数错误")
        else:
            # 完善站点信息
            self.create_update_stations(bus_info=bus_info)
            # 完善ajax_data
            if not bus_info.ajax_data:
                self.get_ajax_data(url=bus_info.real_url, bus_info=bus_info)
            # 获取实时信息
            real_info = grab_real_info(data=bus_info.ajax_data)
            real_info_dict = {}
            for i in real_info:
                real_info_dict[int(i.get("nearstationid", -1))] = i
            # 获取站点信息
            stations_list = BusStations.objects.filter(is_active=True, bus=bus_info)
            serializer = GetBusStationsSerializer(stations_list, many=True, context={"real_info": real_info_dict})
            return SuccessHR(serializer.data)

    def create_update_stations(self, bus_info):
        """创建或更新站点信息"""
        current_time = datetime.datetime.now()
        # 未获取站点信息或者3天未更新，则获取站点信息
        if not bus_info.has_stations or not bus_info.update_time or current_time.day - bus_info.update_time.day >= 3:
            result = grab_bus_real_info(pk=bus_info.id.hex, url=bus_info.real_url)
            need_add_obj = []
            # 更新/创建数据
            exists_stations_id = [i.station_id for i in
                                  BusStations.objects.filter(is_active=True, bus=bus_info)]
            for inx, i in enumerate(result):
                station_id = int(i.get("station_id"))
                name = i.get("name")
                # 此策略在即使已经存在站点信息的情况下，仍然可以对数据进行新增
                if station_id in exists_stations_id:
                    # 更新
                    raw = BusStations.objects.filter(is_active=True, bus=bus_info,
                                                     station_id=station_id).update(name=name)

                else:
                    # 新增
                    need_add_obj.append(BusStations(
                        bus=bus_info,
                        name=i.get("name"),
                        station_id=i.get("station_id"),
                        order=inx + 1,
                    ))
            BusStations.objects.bulk_create(need_add_obj)
            bus_info.has_stations = True
            bus_info.update_time = current_time
            bus_info.save()
        return True

    def get_ajax_data(self, url, bus_info: BusInfo):
        """获取ajax data"""
        ajax_data = grab_ajax_data(real_url=url)
        bus_info.ajax_data = ajax_data
        bus_info.save()


class TestViewToSocket(BaseAPIView, generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        msg = request.data.get("msg", "无内容")
        ViewSocket.group_send(channel_name="chat", event=self.get_event(msg=msg))
        return SuccessHR("已发送")

    def get_event(self, msg):
        return {
            "type": "p.chat",
            "msg": msg
        }
