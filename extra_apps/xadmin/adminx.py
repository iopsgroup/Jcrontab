import xadmin
from xadmin.models import UserSettings
from xadmin.layout import *
from Jcrontab.models import Demandorder


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = True
xadmin.site.register(UserSettings, UserSettingsAdmin)


class DemandorderAdmin(object):
    list_display = ('id','starttime', 'endtime', 'workcycle','subworkcycle','workowner','extname','workcontent','noticeurl','status','ispush','workmode','command')

xadmin.site.register(Demandorder, DemandorderAdmin)