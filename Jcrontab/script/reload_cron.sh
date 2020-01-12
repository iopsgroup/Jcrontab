#!/bin/sh
#Email:jeson@imoocc.com

if [ ! -n "$1" ]; then
    echo "PATH IS NULL"
    mpath=./manage.py
else
    mpath=$1/manage.py
fi

echo "...........">>/opt/codes/logs/Trac.log

while true
do
    /usr/bin/python3 ${mpath} crontab remove &>>/opt/codes/logs/Trac.log
    if [ $? -eq 0 ]
    then
        break
    fi
done
/usr/bin/python3 ${mpath} crontab add &>>/opt/codes/logs/Trac.log