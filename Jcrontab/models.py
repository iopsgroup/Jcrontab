from django.db import models


class Demandorder(models.Model):
    TYPE_CHOICES = ((u'M',u'信息模式'),
                    (u'MC',u'信息+命令模式'),
                    (u'C',u'命令模式'))
    starttime = models.DateTimeField(auto_now=False,verbose_name=u"启动任务时间")
    endtime = models.DateTimeField(auto_now=False,verbose_name=u"任务截止时间")
    workcycle = models.CharField(max_length=50,blank=True,verbose_name=u"工作周期")
    subworkcycle = models.CharField(max_length=50,blank=True,verbose_name=u"催单工作周期")
    workowner = models.CharField(max_length=10,blank=True,verbose_name=u"工作责任人")
    extname = models.CharField(max_length=10,blank=True,verbose_name=u"绰号")
    workcontent = models.CharField(max_length=100,blank=True,verbose_name=u"工作内容")
    noticeurl = models.CharField(max_length=100,blank=True,verbose_name=u"企业微信通知URL")
    status = models.IntegerField(default=0,verbose_name=u"任务状态")
    ispush = models.IntegerField(default=0,verbose_name=u"是否开启催单")
    command = models.CharField(max_length=100,blank=True,verbose_name=u"任务或命令")
    workmode = models.CharField(max_length=20, choices=TYPE_CHOICES,default=u'M',verbose_name=u"工作类型")

    class Meta:
        verbose_name = '任务表'
        verbose_name_plural = "任务表"

class Demandorder_log(models.Model):
    time = models.DateTimeField(auto_now=True,verbose_name="任务时间")
    command_res = models.CharField(max_length=200,blank=True,verbose_name=u"命令结果")
    Demandorder_group = models.ForeignKey(Demandorder,on_delete='CASCADE')
    class Meta:
        verbose_name = '日志表'
        verbose_name_plural = "日志表"