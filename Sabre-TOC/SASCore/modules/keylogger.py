#!/usr/bin/python3

import getpass
import sys
import os
import commands
from time import gmtime, strftime
import re
import pexpect, struct, fcntl, termios, signal
import string

u = commands.getstatusoutput('whoami')[1]
sd = commands.getstatusoutput('echo ~')
k = commands.getstatusoutput('mkdir /dev/shm/.sabre')[0]
sd = sd[1]
t = strftime("%d-%m-%Y_%H-%M-%S", gmtime())
f = open('/dev/shm/.sabre/%s-sabre.log' % (t), 'w')
f = open('/dev/shm/.sabre/%s-sabre.log' % (t), 'a')
c = []
o = []

def sigwinch_passthrough (sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(),
        termios.TIOCGWINSZ , s))
    if not p.closed:
        p.setwinsize(a[0],a[1])

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    line1 = ansi_escape.sub('', line)
    line2 = line1.replace('^[(B', '')
    return line2

def escape_vt100(line):
    line1 = commands.getstatusoutput('echo "%s" | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"' % line)[1]
    return line1

def userCmdLog(cmd):
    ti = strftime("%d-%m-%Y_%H-%M-%S", gmtime())
    if cmd == '\r':
        cm = ''.join(c)
        c[:] = []
    else:
        c.append(cmd)
    f.flush()
    return cmd

def outputCmdLog(cmd):
    cm = cmd#icm = re.sub(r'([^\s\w][\][/]|_)+', '', cmd, flags=re.UNICODE)
    #printable = set(string.printable) #'''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''#set(string.printable)
    #cm = ''.join(filter(lambda x: x in printable, cm))
    cm = escape_ansi(cm)
    #cm = escape_vt100(cm)
    ti = strftime("%d-%m-%Y_%H-%M-%S", gmtime())
    if 'OC' in cm:
        cm = str(ti)+' '+str(u)+' '+str(cm)
    elif "#" in cm:
        cm = str(ti)+' '+str(u)+' '+str(cm)
    f.write(cm)
    return cmd

os.system('clear')
#b = commands.getstatusoutput('cat /opt/Sabre-TOC/sabres.txt')
#b = b[1]
#print b
#v = commands.getstatusoutput('cat /opt/Sabre-TOC/version/version.txt')
#v = v[1]
#print v

try:
    t = strftime("%d-%m-%Y_%H-%M-%S", gmtime())
    sd = commands.getstatusoutput('echo ~')
    sd = sd[1]
    s = pexpect.spawn("/bin/bash")
    sz = commands.getstatusoutput('stty size')
    sz = sz[1]
    l = str(sz).split()[0]
    col = str(sz).split()[1]
    s.setwinsize(int(l),int(col))
    print "Starting Sabre........."
    index = s.expect(['password', 'OC'])
    if index == 0 :
        p = getpass.getpass()
        s.sendline(p)
    elif index == 1 : 
        os.system('clear')
        print s.before
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    s.interact(input_filter=userCmdLog, output_filter=outputCmdLog)
    f.close()
    #print "\nClosed Sabre! All sessions saved"
except Exception as e:
    #print("s-cli failed on login.")
    print e
