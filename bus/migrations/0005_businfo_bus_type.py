# Generated by Django 2.2.7 on 2019-11-24 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0004_auto_20191124_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='businfo',
            name='bus_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bus.BusTypeArea', verbose_name='公交类型'),
        ),
    ]
