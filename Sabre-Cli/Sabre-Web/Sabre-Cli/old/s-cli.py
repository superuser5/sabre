#!/usr/bin/python

import pexpect
import getpass
import sys
import os
import commands
from time import gmtime, strftime

try:
    t = strftime("%d-%m-%Y_%H-%M-%S", gmtime())
    sd = commands.getstatusoutput('echo ~')
    sd = sd[1]
    s = pexpect.spawn('sudo sabre')
    print "Starting Sabre........."
    index = s.expect(['password', 'OC'])
    if index == 0 :
        p = getpass.getpass()
        s.sendline(p)
    elif index == 1 : 
        os.system('clear')
        print s.before
    fout = open('%s/.sabre/%s-sabre-cli.log' % (sd, t), 'wb')
    s.logfile = fout
    s.interact()
    print "\nClosed Sabre Connection!"
except:
    print("s-cli failed on login.")
