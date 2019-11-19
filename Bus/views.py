from django.shortcuts import render, HttpResponse
from rest_framework import generics

from spider.bus import bus_yy


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


class GetBusStations(generics.ListAPIView):
    """
    获取公交车站点
    """

