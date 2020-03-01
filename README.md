# Jcrontab
Jcrontab是一套基于python3.6+django1.8开发实现的前后台界面化的定时任务系统，它打通企业微信消息推送接口，能提供定时的消息推送功能。

## 功能介绍
这个小工程共分为3个小系统。分别为：
### 前端任务系统
前端任务系统，主要记录单个任务执行情况(如：执行时间、任务执行结果等)。  
控制单个任务部分必要属性(如：任务终止启动、任务提醒频率周期修改等)。  
访问路径示例：
http://www.jesonc.com/taskid+数字

### 后台管理系统
后台任务机型基于xadmin的模块，主要用于编辑、添加、删除所有任务。  
访问路径示例：
http://www.jesonc.com/xadmin

### 任务脚本录入系统
这是一个python的脚本(insert_work.py)，用于运维人员方便的在终端新建任务。


## 部署方式
### 安装基础服务  
1、基础程序
Mysql5.7
Python3.6  
nginx-1.16.1  
  
2、安装模块  
Django1.8  
工程所需必要安装模块  
pip -r install ./requirements.txt

### 初始化Mysql及配置  
1、my.cnf设置数据库字符集
character_set_server=utf8

2、mysql数据库及新建用户：  
create database jcrontab;  
CREATE USER jeson@'%' IDENTIFIED BY 'jesonc.com';  
grant all privileges on jcrontab.* to  'jeson'@'%' with grant option;    

3、修改djang配置settings.py中数据库配置信息
DATABASES = {  
        'default': {  
        'ENGINE': 'django.db.backends.mysql',   # 数据库引擎  
        'NAME': 'jcrontab',  # 数据库名，先前创建的  
        'USER': 'jeson',     # 用户名，可以自己创建用户  
        'PASSWORD': 'jesonc.com',  # 密码  
        'HOST': '127.0.0.1',  # mysql服务所在的主机ip  
        'PORT': '3306',         # mysql服务端口  
        }  
}
  
4、初始化数据库模型 
1）注释settings.py下的如下配置
CRONJOBS = todo()
if CRONJOBS is None:
    CRONJOBS = []
2）初始化数据库模型
python3.6 manage.py makemigrations  
python3.6 manage.py migrate
3）打开（1）之前的注释

### 创建xadmin后台用户密码
python3.6 manage.py createsuperuser

Username (leave blank to use 'jeson'): jeson 
Email address: jeson@imoocc.com
Password: jesonc.com
Password (again): jesonc.com
Superuser created successfully.

### 启动工程
python3.6 manage.py runserver  
...持续更新  
![图片名称](http://imoocc.com/static/zinnia_bootstrap/img/weixin.jpg)  
关于更多信息交流，欢迎关注我的公众账号:mukelaoshi或邮件联系jeson@imoocc.com  
