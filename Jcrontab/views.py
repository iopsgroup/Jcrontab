from django.views.generic import CreateView,FormView,ListView
from .models import Person,Demandorder,Demandorder_log
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import render_to_response
import json
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR
SCRIPT_DIR =  BASE_DIR + '/Jcrontab/script'


def tasklistView(request,taskid):
    '''
    任务列表页
    :param request:
    :param taskid:
    :return:
    '''
    tasks = Demandorder_log.objects.filter(Demandorder_group_id=taskid).all().select_related()
    if tasks:
        taskitems = reversed(tasks)

        taskname = tasks[0].Demandorder_group.workcontent
        taskcycle = tasks[0].Demandorder_group.subworkcycle
        taskid = tasks[0].Demandorder_group.id
        taskstatus = tasks[0].Demandorder_group.status
    else:
        taskitems = []
        task = Demandorder.objects.get(id=taskid)
        taskname = task.workcontent
        taskcycle = task.subworkcycle
        taskid = task.id
        taskstatus = task.status
    return render_to_response('task_list.html',{'queryset':taskitems,'taskname':taskname,'taskcycle':taskcycle,'taskid':taskid,'taskstatus':taskstatus})

def taskfinshView(request):
    '''
    任务完成接口
    :param request:
    :return:
    '''
    if request.method == 'POST':
        data = request.POST
        change_status = int(data.get('status'))
        taskid = int(data.get('taskid'))
        taskitem = Demandorder.objects.get(id=taskid)
        print(taskitem.status)
        if taskitem.status == 0:
            taskitem.status = change_status
            taskitem.save()
            return_str = u"谢谢，此单已结！"
            return HttpResponse(return_str)
        else:
            return_str = u"此单已结"
            return HttpResponse(return_str)
        # recive_data = json.loads(request.body)
        # print(recive_data)

def taskrestoreView(request):
    '''
    恢复任务接口
    :param request:
    :return:
    '''
    if request.method == 'POST':
        data = request.POST
        change_status = int(data.get('status'))
        taskid = int(data.get('taskid'))
        taskitem = Demandorder.objects.get(id=taskid)
        print(taskitem.status)
        if taskitem.status == 0:
            return_str = u"此单已在运行！"
            return HttpResponse(return_str)
        else:
            taskitem.status = change_status
            taskitem.save()
            os.system('/bin/sh %s/reload_cron.sh %s'%(SCRIPT_DIR,BASE_DIR))
            return_str = u"此单已恢复提醒！"
            return HttpResponse(return_str)
        # recive_data = json.loads(request.body)
        # print(recive_data)

def tasknewcycleView(request):
    '''
    控制任务周期接口
    :param request:
    :return:
    '''
    if request.method == 'POST':
        data = request.POST
        change_cycle = data.get('newcycle')
        taskid = int(data['taskid'])
        taskid = int(data.get('taskid'))
        ispushed = int(data.get('ispushed'))
        taskitem = Demandorder.objects.get(id=taskid)
        if taskitem:
            taskitem.subworkcycle = change_cycle
            taskitem.ispush = ispushed
            taskitem.save()
            os.system('/bin/sh %s/reload_cron.sh %s'%(SCRIPT_DIR,BASE_DIR))
            return_str = u"已修改催单周期为%s！"%change_cycle
            return HttpResponse(return_str)

def tasknopushView(request):
    '''
    恢复原始任务周期接口
    :param request:
    :return:
    '''
    if request.method == 'POST':
        data = request.POST
        taskid = int(data.get('taskid'))
        ispushed = int(data.get('ispushed'))
        taskitem = Demandorder.objects.get(id=taskid)
        if taskitem:
            taskitem.ispush = ispushed
            taskitem.subworkcycle = ''
            taskitem.save()
            os.system('/bin/sh %s/reload_cron.sh %s'%(SCRIPT_DIR,BASE_DIR))
            return_str = u"已恢复原始周期！"
            return HttpResponse(return_str)
