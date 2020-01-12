#!/bin/sh
#Email:jeson@imoocc.com

if [ ! -n "$1" ]; then
    echo "PATH IS NULL"
    mpath=./manage.py
else
    mpath=$1/manage.py
fi


/usr/bin/python3 /opt/codes/Jtrac/manage.py crontab show
if [ $? -ne 0 ]
then
    killall python3
fi


ps -ef|grep manage.py|grep -v grep|grep -v crontab
if [ $? -ne 0 ]
then
    /usr/bin/python3 ${mpath} runserver 127.0.0.1:1080 &>>/opt/codes/logs/Trac.log &
    while true
    do
        /usr/bin/python3 ${mpath} crontab remove
        if [ $? -eq 0 ]
        then
            break
        fi
    done
    /usr/bin/python3 ${mpath} crontab add
    echo "start process..."
else
    echo "Already runing...."
fi
