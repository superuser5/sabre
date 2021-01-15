#!/usr/bin/python3

import subprocess
import sys
import pexpect
import json
import argparse

parser = argparse.ArgumentParser(description='Connect to MSFRPC for MSF console session.')
parser.add_argument('-U', '--user', required=True, help='User Name to log into MSFRPC')
parser.add_argument('-P', '--passwd', required=True, help='User Name to log into MSFRPC')
parser.add_argument('-S', '--server', required=True, help='IP or Domain Name to connect to for MSFRPC')
args = parser.parse_args()

u = args.user
passwd = args.passwd
ip = args.server

p = pexpect.spawn('msfrpc -U %s -P %s -a %s' % (u,passwd,ip))
print('Connecting')
p.expect('>>')
#print 'Got Prompt'
p.sendline("rpc.call('console.create')\n")
p.expect('>>')
print('Ready')
t = p.before.split('\n')
t = t[1]
print(t)
t = t.split(',')
print('Console ID is: ' + t[0][11:-1])
i = t[0][11:-1]        #raw_input('ID Number: ')
prompt = 'msf5'
p.sendline(r'rpc.call("console", "%s", "%s\n")' % (i,'\n'))
p.sendline('rpc.call("console.read", "%s")' % i)

while True:
	c = input("%s# " % prompt)
	if c == 'exit':
		exit()
	s = r'rpc.call("console.write", "%s", "%s\n")' % (i,c)
	p.sendline(s)
	p.expect('>>') 
	p.sendline('rpc.call("console.read", "%s")' % i)
	p.expect('>>') 
	o = p.before
	#o = o[3:]
	#o = o.split('\n')
	#o = o[1]
	#o = o[2:]
	#o = o.split(',')
	prompt = str(o) #[1][12:]
	prompt = prompt.replace(r'\x01\x02','')
	d = o[0][11:]
	d = d.split(r'\n')
	for l in d:
		print(l)
