# Generated by Django 2.0.6 on 2020-04-16 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0009_busstations_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='businfo',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='排序'),
        ),
    ]
