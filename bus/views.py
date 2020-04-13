import json
from collections import OrderedDict

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from rest_framework import generics
from rest_framework.response import Response

from bus.models import BusInfo
from bus.serializers import GetBusStationsSerializer
from base.views import BaseAPIView
from spider.bus import bus_yy
from common.return_tool import SuccessHR


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


class GetBusStations(BaseAPIView, generics.ListAPIView):
    """
    get bus stations
    """
    queryset = BusInfo.objects.filter().order_by('bus_type', 'number', 'visit_traffic')
    serializer_class = GetBusStationsSerializer

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
        result = OrderedDict()
        for i in result_queryset:
            number = i.number[:i.number.find("路")+1] if i.number.find("路") else i.number
            result.setdefault(number, GetBusStationsSerializer(i).data)

        page = self.paginate_queryset(list(result.values()))
        if page is not None:
            return self.get_paginated_response(page)

        return SuccessHR(self.get_serializer(result_queryset.all(), many=True).data)
