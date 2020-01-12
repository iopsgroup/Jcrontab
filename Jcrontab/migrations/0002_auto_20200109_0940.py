# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Jcrontab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandorder',
            name='command_con',
            field=models.CharField(verbose_name='任务或命令', max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='demandorder',
            name='workmode',
            field=models.CharField(max_length=20, default='M', choices=[('M', '信息模式'), ('MC', '信息+命令模式'), ('C', '命令模式')]),
        ),
        migrations.AddField(
            model_name='demandorder_log',
            name='command_res',
            field=models.CharField(verbose_name='命令', max_length=200, blank=True),
        ),
    ]
