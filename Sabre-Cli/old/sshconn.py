#!/usr/bin/python

import subprocess
import sys
import os

f = open('/etc/Sabre/sabres.txt', 'r')
for i in f:
	print i
f.close

hip = os.environ['TOC']
subprocess.call(['ssh', '-i', '/etc/Sabre/TSKEY', 'root@%s' % hip, '-t', 'sabre; bash -l'])
