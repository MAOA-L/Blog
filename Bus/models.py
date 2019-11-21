from django.db import models

from base.models import Base


class BusInfo(Base):
    """
    公交
    """
    number = models.CharField(verbose_name="公交号", max_length=32)
    departure_station = models.CharField(verbose_name="始发站", max_length=255)
    destination = models.CharField(verbose_name="终点站", max_length=255)


class BusStations(Base):
    """
    公交车站信息
    """
    bus = models.ForeignKey("BusInfo", verbose_name="所属公交", on_delete=models.CASCADE, related_name="%(class)s_bus")
    name = models.CharField(verbose_name="公交站名", max_length=180)
    station_id = models.PositiveSmallIntegerField(verbose_name="站点id", null=True)
    lon = models.CharField(verbose_name="经度", max_length=32)
    lat = models.CharField(verbose_name="纬度", max_length=32)
