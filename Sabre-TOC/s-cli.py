#!/usr/bin/python3

import getpass
import sys
import os
import subprocess
from time import gmtime, strftime, localtime
import re
import pexpect, struct, fcntl, termios, signal
import string
import subprocess
#import sh
#from multiprocessing import Process

u = subprocess.getstatusoutput('whoami')[1]
sd = subprocess.getstatusoutput('echo ~')
sd = sd[1]
t = strftime("%d-%m-%Y_%H-%M-%S", localtime())
f = open('%s/.sabre/%s-sabre.log' % (sd, t), 'w')
f = open('%s/.sabre/%s-sabre.log' % (sd, t), 'a')
c = []
o = []
pmt = ''
setPrompt=''
logme = ''
init = True


def sigwinch_passthrough (sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(),
        termios.TIOCGWINSZ , s))

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    line1 = ansi_escape.sub('', line)
    line2 = line1.replace('^[(B', '')
    return line2

def escape_vt100(line):
    line1 = subprocess.getstatusoutput('echo "%s" | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"' % line)[1]
    return line1

def userCmdLog(cmd):
    global pmt
    global init
    global logme
    global setPrompt
    ti = strftime("%d-%m-%Y %H:%M:%S", localtime())
    if cmd == '\r':
        cm = ''.join(c)
        c[:] = []
        if setPrompt == 'session_':
            pmt = setPrompt+cm+':'
            setPrompt = ''
        if cm == 'sessions' or cm == 'ses' or cm == 'sess' or cm == 'sessi' or cm == 'sessio' or cm == 'session':
            setPrompt = 'session_'
        cm = str(ti)+' '+str(u)+':'+' '+pmt+' '+str(cm)
        if init == False:
            logme = logme + '\n    <\output>\n<\command>'
            parse = logme.split('\n')
            if parse[-1] == '<\command>':
                    writeme = '\n'.join(parse)
                    f.write(writeme)
                    f.flush()
                    logme = ''
        if init == True:
            init = False
        logme = logme + '\n<command>    %s\n    <output>' % cm
    else:
        c.append(cmd)
    return cmd

def outputCmdLog(cmd):
    global pmt
    global logme
    cm = cmd
    cm = escape_ansi(cm)
    ti = strftime("%d-%m-%Y %H:%M:%S", localtime())
    if 'OC' not in cm:
        if '\n' in cm or '\r' in cm:
            logme = logme + '%s' % cm
    elif 'OC' in cm:
        pmt = cm.split('\n')[0]
    return cmd

os.system('clear')
b = subprocess.getstatusoutput('cat /opt/Sabre-TOC/sabres.txt')
b = b[1]
print(b)
v = subprocess.getstatusoutput('cat /opt/Sabre-TOC/version/version.txt')
v = v[1]
print(v)

try:
    t = strftime("%d-%m-%Y_%H-%M-%S", localtime())
    sd = subprocess.getstatusoutput('echo ~')
    sd = sd[1]
    s = pexpect.spawn("sudo -E /opt/Sabre-TOC/main.py")
    sz = subprocess.getstatusoutput('stty size')
    sz = sz[1]
    l = str(sz).split()[0]
    col = str(sz).split()[1]
    s.setwinsize(int(l),int(col))
    #sabreConnProc = Process(target=sabreConnFunc)
    #sabreConnProc.start()
    #sabreNativeConnProc = Process(target=sabreNativeConnFunc)
    #sabreNativeConnProc.start()
    print("Starting Sabre.........")
    index = s.expect(['password', 'OC'])
    if index == 0 :
        p = getpass.getpass()
        s.sendline(p)
    elif index == 1 : 
        os.system('clear')
        print(s.before)
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    s.interact(input_filter=userCmdLog, output_filter=outputCmdLog)
    f.close()
    print("\nClosed Sabre! All sessions saved")
except Exception as e:
    print("s-cli failed on login.")
    print(e)
