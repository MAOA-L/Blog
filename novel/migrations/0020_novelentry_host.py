# Generated by Django 3.0.5 on 2020-05-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0019_remove_novelentry_content_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='novelentry',
            name='host',
            field=models.CharField(max_length=255, verbose_name='小说网站host'),
            preserve_default=False,
        ),
    ]