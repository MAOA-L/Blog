# Generated by Django 2.2.7 on 2019-11-22 12:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='上次修改时间')),
                ('ip_addr', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('number', models.CharField(max_length=32, verbose_name='公交号')),
                ('departure_station', models.CharField(max_length=255, verbose_name='始发站')),
                ('destination', models.CharField(max_length=255, verbose_name='终点站')),
                ('visit_traffic', models.IntegerField(default=0, verbose_name='访问量')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BusStations',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, primary_key=True, serialize=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('gmt_created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='上次修改时间')),
                ('ip_addr', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('name', models.CharField(max_length=180, verbose_name='公交站名')),
                ('station_id', models.PositiveSmallIntegerField(null=True, verbose_name='站点id')),
                ('lon', models.CharField(max_length=32, verbose_name='经度')),
                ('lat', models.CharField(max_length=32, verbose_name='纬度')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='busstations_bus', to='bus.BusInfo', verbose_name='所属公交')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]