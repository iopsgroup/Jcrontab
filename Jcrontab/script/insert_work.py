#!/usr/local/bin/python3
#Email:jeson@imoocc.com

import os,sys,django
import datetime

parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Jcron.settings')
django.setup()
from Jcrontab.models import Demandorder
from Jcrontab.utils.cron_list import sendinfo,todo

new_starttime = ''
if not new_starttime:
    new_starttime = datetime.date.today()

contents_all = [i.workcontent for i in Demandorder.objects.all()]
worklist = [
    {"new_starttime":new_starttime,
    "new_endtime":'2019-11-20',
    "new_workcycle":'*/2 * * * *',
    "new_owner":'jesonc,',
    "new_workconntent":'xxx任务',
    "new_noticeurl":'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx',
    "new_extname":'牧客'},
]

for item in worklist:
    if item['new_workconntent'] in contents_all:
        print("%s 已存在此工作任务"%item['new_workconntent'])
        continue
    print(item)
    n1=Demandorder(
        starttime = new_starttime,
        endtime = item['new_endtime'],
        workcycle = item['new_workcycle'],
        workowner = item['new_owner'],
        workcontent = item['new_workconntent'],
        noticeurl = item['new_noticeurl'],
        extname = item['new_extname']
    )
    n1.save()
    itemcronjob = todo(itemw=n1,title="【建单通知】")
    taskid = n1.id
    sendinfo(itemcronjob[1],taskid)


