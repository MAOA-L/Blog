# Generated by Django 2.0.6 on 2020-04-22 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0010_businfo_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='businfo',
            name='ajax_data',
            field=models.CharField(max_length=255, null=True, verbose_name='获取实况的异步data'),
        ),
    ]
