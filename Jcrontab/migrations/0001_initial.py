# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Demandorder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('starttime', models.DateTimeField(verbose_name='启动任务时间')),
                ('endtime', models.DateTimeField(verbose_name='任务截止时间')),
                ('workcycle', models.CharField(verbose_name='工作周期', max_length=50, blank=True)),
                ('subworkcycle', models.CharField(verbose_name='催单工作周期', max_length=50, blank=True)),
                ('workowner', models.CharField(verbose_name='工作责任人', max_length=10, blank=True)),
                ('extname', models.CharField(verbose_name='绰号', max_length=10, blank=True)),
                ('workcontent', models.CharField(verbose_name='工作内容', max_length=100, blank=True)),
                ('noticeurl', models.CharField(verbose_name='企业微信通知URL', max_length=100, blank=True)),
                ('status', models.IntegerField(verbose_name='当前处理状态', default=0)),
                ('ispush', models.IntegerField(verbose_name='是否开启催单', default=0)),
            ],
            options={
                'verbose_name': '任务表',
                'verbose_name_plural': '任务表',
            },
        ),
        migrations.CreateModel(
            name='Demandorder_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.DateTimeField(verbose_name='日志时间', auto_now=True)),
                ('Demandorder_group', models.ForeignKey(on_delete='CASCADE', to='Jcrontab.Demandorder')),
            ],
            options={
                'verbose_name': '日志表',
                'verbose_name_plural': '日志表',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=130)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('job_title', models.CharField(max_length=30, blank=True)),
                ('bio', models.TextField(blank=True)),
            ],
        ),
    ]
