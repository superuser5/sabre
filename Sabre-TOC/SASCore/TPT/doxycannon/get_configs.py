#!/usr/bin/python3

import os
import sys
import commands

def choices(arg):
        switch = {
                1: 'https://www.privateinternetaccess.com/openvpn/openvpn.zip',
                2: 'https://www.privateinternetaccess.com/openvpn/openvpn-windows-block-outside-dns.zip',
                3: 'https://www.privateinternetaccess.com/openvpn/openvpn-strong.zip',
                4: 'https://www.privateinternetaccess.com/openvpn/openvpn-ip.zip',
                5: 'https://www.privateinternetaccess.com/openvpn/openvpn-tcp.zip',
                6: 'https://www.privateinternetaccess.com/openvpn/openvpn-strong-tcp.zip',
                7: 'https://www.privateinternetaccess.com/openvpn/openvpn-ip-lport.zip',
                8: 'https://www.privateinternetaccess.com/openvpn/openvpn-ip-tcp.zip',
        }
        return switch.get(arg, 'Invalid')


print 'Select what configs you would like to use for doxycannon, ***Last two are legacy***'

f = open('./vpn_files.txt', 'r')
c = 1
for i in f:
	print str(c) + str(i)
	c = c + 1

f.seek(0)
s = raw_input('Select a number(1): ') or "1"
u = choices(int(s))
print 'Getting config files from: %s' % u
os.system('wget %s' %u)
os.system('mkdir VPN')
os.system('mv openvpn.zip VPN/')
os.system('unzip VPN/openvpn.zip -d VPN/')

print ''
s = raw_input('Input you VPN Username: ')
os.system('echo "%s" >> VPN/auth.txt' % s)
s = raw_input('Input you VPN Password: ')
os.system('echo "%s" >> VPN/auth.txt' % s)
l = commands.getstatusoutput('ls -1 VPN/ | grep ovpn')
for i in l:
	os.system('echo "%s" >> ' % i)
