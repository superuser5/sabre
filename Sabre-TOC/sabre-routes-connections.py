#!/usr/bin/python3

import sys
import subprocess
from time import strftime, localtime, sleep
import hashlib
f = open('/home/root/.sabre/native-connections.log', 'w+')
hostname = subprocess.check_output('hostname', shell=True)
while True:
    conns = subprocess.check_output("netstat -tn 2>/dev/null | grep -v :22 | grep -v 127.0.0 | grep -v server | grep -v Address | awk '{print $5}' | sort | uniq -c | sort -nr | head", shell=True)
    date = strftime("%d-%m-%Y %H:%M:%S", localtime())
    conns = conns.split('\n')
    for i in conns:
        n = hashlib.sha1()
        n.update(str(date) + str(i))
        nonce = n.hexdigest() #base64.b64encode(str(date) + str(i))
        if i != '':
            output = '<command>    %s nativeconnections: non-interactive: \n    <output>\n%s - %s - %s\n    <\output>\n<\command>\n' % (date,hostname[:-1],i,nonce)
            print(output)
            f.write(output)
            f.flush()
    sleep(5)

