#!/bin/sh
#Email:jeson@imoocc.com

rsync -avzP -e 'ssh -i /opt/key/jesonc.com' /Users/jeson/PycharmProjects/Jcron root@jesonc.com:/opt/codes