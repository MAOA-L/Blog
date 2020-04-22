from django.db import models

from base.models import Base


class BusTypeArea(Base):
    """
    公交类型区域
    """
    name = models.CharField(verbose_name="类型名", max_length=32)


class BusInfo(Base):
    """
    bus
    """
    number = models.CharField(verbose_name="公交号", max_length=32)
    departure_station = models.CharField(verbose_name="始发站", max_length=255, null=True)
    destination = models.CharField(verbose_name="终点站", max_length=255, null=True)
    visit_traffic = models.IntegerField(verbose_name="访问量", default=0)
    code = models.CharField(verbose_name="公交辨识码", max_length=32, null=True)
    bus_type = models.ForeignKey(BusTypeArea, verbose_name="公交类型", on_delete=models.SET_NULL, null=True)
    grab_real_url = models.CharField(verbose_name="用来获取实况信息的url", max_length=255)
    real_url = models.CharField(verbose_name="获取实况信息的url", max_length=255, null=True)
    ajax_data = models.CharField(verbose_name="获取实况的异步data", max_length=255, null=True)
    has_stations = models.BooleanField(verbose_name="是否已经存在站点信息", default=False)
    update_time = models.DateField(verbose_name="更新站点信息的时间", null=True)
    order = models.PositiveSmallIntegerField(verbose_name="排序", default=0)


class BusStations(Base):
    """
    bus stations info
    """
    bus = models.ForeignKey("BusInfo", verbose_name="所属公交", on_delete=models.CASCADE, related_name="%(class)s_bus")
    name = models.CharField(verbose_name="公交站名", max_length=180)
    station_id = models.PositiveSmallIntegerField(verbose_name="站点id", null=True)
    lon = models.CharField(verbose_name="经度", max_length=32)
    lat = models.CharField(verbose_name="纬度", max_length=32)
    order = models.PositiveSmallIntegerField(verbose_name="站点排序", default=0)
