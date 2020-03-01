#!/usr/local/bin/python3

import urllib.request
import urllib.parse
# import urllib3
import ssl
import requests
import json
import os,sys
import django
import time
from datetime import tzinfo, timedelta, datetime
import pytz
import base64
import hashlib
import subprocess
# parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(parent_path)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Jcron.settings')
# django.setup()
# from Jcrontab.models import Demandorder
from django.conf import settings
BASE_DIR = settings.BASE_DIR
from Jcrontab.models import Demandorder, Demandorder_log

ssl._create_default_https_context = ssl._create_unverified_context

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Jcron.settings')
django.setup()

def recordlog(taskid):
    '''
    方法：用于记录日志
    :param taskid:
    :return:
    '''
    Demandorder_log.objects.create(Demandorder_group_id=taskid)

def record_command_res(taskid,res):
    '''
    方法：用于记录任务返回的结果
    :param taskid:
    :param res:
    :return:
    '''
    Demandorder_log.objects.create(Demandorder_group_id=taskid,command_res=res)


def sendinfo(data,taskid):
    '''
    方法：通过调用企业微信接口发送文本、图片(调用sendimg接口)信息
    :param data:
    :param taskid:
    :return:
    '''

    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)',
        # 'Host': 'jesonc.com',
        'Content-Type':'text/plain'
    }
    check_its = Demandorder.objects.get(id=taskid)
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)
    if check_its.status == 0 and check_its.endtime > now and now > check_its.starttime:
        url = check_its.noticeurl
        res = requests.post(url=url,json=data,headers=headers)
        recordlog(taskid)
        if check_its.ispush == 1:
            sendimg(imgpath='%s/sendimgs/cuidan.png'%settings.STATICFILES_DIRS[0],url=url)
        else:
            sendimg(imgpath='%s/sendimgs/jiandan.png'%settings.STATICFILES_DIRS[0], url=url)


def getinfo(itemw,title='【通知需求】',change_cycle=''):
    '''
    方法：获取发送信息的模版
    :param itemw:
    :param title:
    :param change_cycle:
    :return:
    '''

    dtime = time.strftime("%Y-%m-%d", time.localtime())
    xtime = time.strftime("%w", time.localtime())
    # readurl = "http://127.0.0.1:8000/taskid%s"%(itemw.id)
    readurl = "http://%s/taskid%s"%(settings.SERVICE_ADDR,itemw.id)
    backurl = "http://%s/xadmin"%settings.SERVICE_ADDR

    send_content = "%s\n%s:今天是%s号 星期%s\n 执行命令:%s\n 结单链接:%s\n 管理后台:%s。\n谢谢!"%(title+itemw.workcontent,itemw.extname,dtime,xtime,itemw.command,readurl,backurl)
    data = {
        "msgtype": "text",
        "text": {
            "content": send_content,
            "mentioned_list":itemw.workowner.split(','),
        }
    }
    if change_cycle:
        CRONJOBS_item = (change_cycle,data)
    else:
        CRONJOBS_item = (itemw.workcycle,data)
    return CRONJOBS_item

def sendimg(imgpath='',url=''):
    '''
    方法：发送通过企业微信群发机器人发送图片
    :param imgpath:
    :param url:
    :return:
    '''

    with open(imgpath, "rb") as f:
        fcontent = f.read()
        md5_data = hashlib.md5(fcontent).hexdigest()
        base64_data = base64.b64encode(fcontent).decode("utf-8")

    data = {
        "msgtype": "image",
        "image": {
            "base64": base64_data,
            "md5": md5_data,
        }
    }

    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)',
        # 'Host': 'jesonc.com',
        'Content-Type':'application/json'
    }
    content_tpye = "\'Content-Type: application/json\'"
    imgdata = json.dumps(data)
    os.system("curl %s -H %s -d '%s'" % (url, content_tpye,imgdata ))

def commad_res(commands='',logfile='',notice_data='',taskid=''):
    '''
    方法：执行具体任务
    :param commands:
    :param logfile:
    :param notice_data:
    :param taskid:
    :return:
    '''
    command_list = set(commands.split())
    black_rules = ('rm','reboot','shutdown')
    equal_sets = command_list.intersection(black_rules)

    check_its = Demandorder.objects.get(id=taskid)
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)
    if check_its.status == 0 and check_its.endtime > now and now > check_its.starttime:
        if commands and not equal_sets:
            try:
                output = subprocess.run(commands, shell=True, stdout=subprocess.PIPE,
                                        universal_newlines=True)
                res = {'code':0,'result':output}
            except Exception as inst:
                res = {'code': 1, 'result': inst}
            with open(logfile,'a') as f:
                res = 'Time:%s,Command:%s,Res:%s'%(datetime.now(),commands,output)
                f.write(res)
                f.close()
            if output.returncode == 0:
                extra_info = "\n -----部分命令执行结果-----\n%s"%output.stdout
            else:
                extra_info = "\n -----部分命令执行结果-----\n%s"%output.stderr
            notice_data['text']['content'] = notice_data['text']['content']+extra_info
            # notice_data['text']['content'] = notice_data['text']['content'] + "\n 部分命令执行结果：%s"%output[0:20]
            sendinfo(data=notice_data,taskid=taskid)

            record_command_res(taskid=taskid,res=extra_info)
            return "ok"


def todo():
    '''
    方法：初始化返回settings.py中CRONTAB所需的自动化任务列表
    :return:
    '''
    cronjobs = [('*/1 * * * *','/script/test2.sh')]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Jcron.settings')
    django.setup()
    tasksall = Demandorder.objects.all()
    taskcout = tasksall.count()
    if taskcout != 0:
        for i in tasksall:
            if i.ispush == 1:
                do_workcycle = i.subworkcycle
            else:
                do_workcycle = i.workcycle
            itemcronjob = getinfo(itemw=i, change_cycle=do_workcycle)
            taskid = i.id

            if i.workmode == u'M':
                itemcronjob = (itemcronjob[0], 'Jcrontab.utils.cron_list.sendinfo', [itemcronjob[1], taskid])
                cronjobs.append(itemcronjob)
            elif i.workmode == u'MC':
                logfile = format(BASE_DIR + '/logs/log_{:%d_%m_%Y}.log'.format(datetime.now()))
                commancronjob = (itemcronjob[0], 'Jcrontab.utils.cron_list.commad_res',[i.command,logfile,itemcronjob[1], taskid],{},'>> %s'%logfile)
                cronjobs.append(commancronjob)
            else:
                pass

    CRONJOBS = cronjobs
    return CRONJOBS

if __name__ == '__main__':
    parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(parent_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Jcron.settings')
    django.setup()

    todo()