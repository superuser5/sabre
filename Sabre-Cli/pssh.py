#!/usr/bin/python3

from pexpect import pxssh
import getpass
import sys
import os
import argparse
import subprocess

# Have it check for a local ssh key, if not then prompt for password authentication and then create a key for the user on the TOC and pull it down to the local user direcotry, then chmod 600 the key


parser = argparse.ArgumentParser(description='Connect to a Sabre Tactical Operations Center (TOC).')
parser.add_argument('-u', '--user', required=True, help='User Name to log into Sabre-TOC')
parser.add_argument('-s', '--server', required=True, help='IP or Domain Name to connect to for Sabre-TOC')
args = parser.parse_args()

keydir = os.path.isdir('~/.ssh')
if keydir == False:
    os.system('mkdir ~/.ssh 2>/dev/null')

sd = subprocess.getstatusoutput('echo ~')
sd = str(sd[1]) + '/.ssh/sabre-key'

key = os.path.isfile(sd)

try:
    s = pxssh.pxssh()
    hostname = args.server #"127.0.0.1"
    username = args.user #'root'

    if key == True:
        sz = subprocess.getstatusoutput('stty size')
        sz = sz[1]
        l = str(sz).split()[0]
        col = str(sz).split()[1]
        s.login(hostname, username, ssh_key=sd)
        os.system('clear')
        print("Confirming Hostname: ")
        s.sendline('hostname')
        print(str(s.before, 'utf-8'))
        print("Confirming User: ")
        s.sendline('whoami')
        s.prompt()
        print(str(s.before, 'utf-8'))
        print("Connected to Sabre-TOC. Use SHIFT-] to exit. This may take a few minutes........")
        s.sendline('sabre')
        #s.prompt()
        print(str(s.before, 'utf-8'))
        s.setwinsize(66,272)
        s.interact()
        print("\nClosed Sabre Connection!")
        s.logout()
        s.close()
        exit()
    else:
        password = getpass.getpass('Password: ')
        s.login(str(hostname), str(username), str(password))
        s.sendline('whoami')
        s.prompt()
        #print(s.before)
        s.sendline('ssh-keygen -N "" -f ~/.ssh/sabre-key')
        s.prompt()
        #print s.before
        s.sendline('cat ~/.ssh/sabre-key')
        s.prompt()
        newkey = str(s.before, 'utf-8')
        print(newkey)
        s.sendline('cat ~/.ssh/sabre-key.pub > ~/.ssh/authorized_keys')
        s.prompt()
        f = open('%s' % sd, 'w+')
        f.write(newkey)
        f.close()
        os.system('chmod 600 ~/.ssh/sabre-key')
        print('Now rerun the Sabre-CLI')
        

except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)

