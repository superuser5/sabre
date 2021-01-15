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
import sh
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
    #if not s.closed:
    #    s.setwinsize(a[0],a[1])

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
            #print('Set prompt to the specific session.')
            #print('Should be this: %s' % cm[:-1])
        if cm == 'sessions' or cm == 'ses' or cm == 'sess' or cm == 'sessi' or cm == 'sessio' or cm == 'session':
            setPrompt = 'session_'
            #print('set session for prompt')
        #cm = '\n'+str(ti)+' '+str(u)+':'+' '+pmt+' '+str(cm)+';;;\n'
        cm = str(ti)+' '+str(u)+':'+' '+pmt+' '+str(cm)
        #f.write(cm)
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
    #f.flush()
    return cmd

def outputCmdLog(cmd):
    global pmt
    global logme
    cm = cmd
    cm = escape_ansi(cm)
    ti = strftime("%d-%m-%Y %H:%M:%S", localtime())
    if 'OC' not in cm:
        if '\n' in cm or '\r' in cm:
            #f.write(cm)
            logme = logme + '%s' % cm
    elif 'OC' in cm:
        pmt = cm.split('\n')[0]
    return cmd



###  This is to start the background logging of all connections to the team server that are SSH
###  clients.
#def sabreConnFunc():
#    try:
#            sabreConn = subprocess.check_output('sudo ps -eaf |grep sabre-connection | grep -v grep', shell=True)
#            print(sabreConn)
#    except:
#            sabreConn = subprocess.check_output('sudo nohup /opt/Sabre-TOC/sabre-connections.py &', shell=True)
#            print(sabreConn)
#    return sabreConn
#
#
###  This is to start the background logging of all connections to the team server that are not SSH
###  but targets reaching back to the server. Eventually this need to also track any new routes placed.
#def sabreNativeConnFunc():
#    try:
#            sabreNativeConn = subprocess.check_output('sudo ps -eaf |grep sabre-native-connection | grep -v grep', shell=True)
#            print(sabreNativeConn)
#    except:
#            sabreNativeConn = subprocess.check_output('sudo nohup /opt/Sabre-TOC/sabre-native-connections.py &', shell=True)
#            print(sabreNativeConn)
#    return sabreNativeConn
#



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
