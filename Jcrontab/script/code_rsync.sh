#!/bin/sh
#Email:jeson@imoocc.com

rsync -avzP -e 'ssh -i /opt/key/jesonc.com -p 9922' /Users/jeson/PycharmProjects/Jcron root@jesonc.com:/opt/codes