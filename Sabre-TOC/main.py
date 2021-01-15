#!/usr/bin/env python3

from cmd2 import Cmd, with_argparser 
import argparse
import subprocess
import redis
import os
import atexit
import readline
from SASCore.TPT.MSF import *
from SASCore.TPT.Empire import *
from SASCore.TPT.PTF import *
from SASCore.TPT.EXTERNAL import *
from SASCore.Listeners.simpleserver import *
from SASCore.Listeners.nativeserver import *
from SASCore.Operators import *
from SASCore.modules.syslogDiscover import *
from scapy.all import *
import subprocess
import time

history_file = os.path.expanduser('~/.OC_history')
if not os.path.exists(history_file):
	with open(history_file, "w") as fobj:
		fobj.write("")
readline.read_history_file(history_file)
atexit.register(readline.write_history_file, history_file)

class HQ(Cmd):
	prompt = 'OC: '
	intro = "Who Dares Wins"

	def __init__(self):
		Cmd.__init__(self)


	def do_exit(self, arg):
		"Exit Sabre-TOC"
		quit()

	def do_reset(self, arg):
		"Reset Sabre-TOC Screen Size"
		os.system(reset)


	def do_listener(self, arg):
		"Go to the listener menu"
		sub_cmd = listeners()
		sub_cmd.cmdloop()

	def do_list_sessions(self, cmd):
		'Get Running Listeners'
		print('Getting Running Listeners')
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
		except:
			print('No Active Sessions')
		    
	def do_killsession(self, cmd):
		'Kill an existing session: msfconsole1 or empire1 etc..'
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session. all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
			s = input('Enter in session ID: ')
			subprocess.call(['tmux', 'kill-session', '-t', s])
		except:
			print('No Active Sessions')

	def do_sessions(self, cmd):
		'Interact with an existing session: msfconsole1 or empire1 etc..'
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
			s = input('Enter in session ID: ')
			subprocess.call(['tmux', 'attach', '-t', s])
		except:
			print('No Active Sessions')

	def do_tpt(self, arg):
		"Go to the TPT menu"
		sub_cmd = TPT()
		sub_cmd.cmdloop()

	def do_operator(self, arg):
		"Go to the operator menu"
		sub_cmd = operator()
		sub_cmd.cmdloop()

	def do_intel(self, arg):
		"Go to the Intel menu"
		sub_cmd = intel()
		sub_cmd.cmdloop()

	def do_auxiliary(self, arg):
		"Go to the Auxiliary Tools Menu"
		sub_cmd = auxiliary()
		sub_cmd.cmdloop()

	def do_checkdb(self, arg):
		"Check for connectivity to the DB"
		global r
		value = r.info()
		if value:
			print("Connected!")
		else:
			print("Disconnected")

##### ALIASES #####
	do_list = do_list_sessions

class listeners(Cmd):
	prompt = 'OC-Listeners: '
	intro = "Who Dares Wins: Who Listens Wins"

	def __init__(self): #, teamserver):
		Cmd.__init__(self)

	def do_exit(self, arg):
		"Exit SABRE-OC"
		quit()

	def do_tpt(self, arg):
		"Go to the TPT menu"
		sub_cmd = TPT()
		sub_cmd.cmdloop()

	def do_operator(self, arg):
		"Go to the operator menu"
		sub_cmd = operator()
		sub_cmd.cmdloop()

	def do_intel(self, arg):
		"Go to the Intel menu"
		sub_cmd = intel()
		sub_cmd.cmdloop()

	def do_auxiliary(self, arg):
		"Go to the Auxiliary Tools Menu"
		sub_cmd = auxiliary()
		sub_cmd.cmdloop()

	def do_checkdb(self, arg):
		"Check for connectivity to the DB"
		global r
		value = r.info()
		if value:
			print("Connected!")
		else:
			print("Disconnected")


#	def do_listListeners(self, cmd):            To add when SIMPLE uses REDIS
#		global r
#		print 'Getting Running Listeners'
#		result = r.lrange('listeners', 0, 100)
#		for i in result:
#			print str(i) 

	argparserlistener = argparse.ArgumentParser()
	argparserlistener.add_argument('-p', '--lport', action="store_true", help='Listening Port')
	argparserlistener.add_argument('-l', '--lhost', action='store_true', help='Listening Host')
	@with_argparser(argparserlistener)
	def do_start_listener(self, args, opts=None):
		'Generates Basic LISTENER: listener -p 443 -l 0.0.0.0'
		print(args)
		global r
		if opts.lhost:
			LHOST = opts.lhost
		else:
			LHOST = '0.0.0.0'
		if opts.lport:
			LPORT = opts.lport
		else:
			LPORT = '443'
		LHOST = input('IP of server:[0.0.0.0] ') or str('0.0.0.0')
		LPORT = input('Port to listen on:[443] ') or int('443')
		iListener = simple(r, LHOST, LPORT)
		iListener.screenSimple()
		print(LHOST)
		print(LPORT)

	def do_native_http(self, args, opts=None):
		'Start a Native Listener for HTTP Session; Default for port 80'
		global r
		LHOST = "0.0.0.0"
		LPORT = input('Port to listen on:[80] ') or int('80')
		nListener = native(r, LHOST, LPORT)
		nListener.screenNative()
		print(LPORT)

	def do_list_sessions(self, cmd):
		'Get Running Listeners'
		print('Getting Running Listeners')
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
		except:
			print('No Active Sessions')

	def do_killsession(self, cmd):
		'Kill an existing session: msfconsole1 or empire1 etc..'
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session. all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
			s = input('Enter in session ID: ')
			subprocess.call(['tmux', 'kill-session', '-t', s])
		except:
			print('No Active Sessions')

	def do_sessions(self, cmd):
		'Interact with an existing session: msfconsole1 or empire1 etc..'
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
			s = input('Enter in session ID: ')
			subprocess.call(['tmux', 'attach', '-t', s])
		except:
			print('No Active Sessions')

##### ALIASES ######
	do_interact = do_sessions
	do_list = do_list_sessions


class TPT(Cmd):
	prompt = 'OC-Third-Party-Tools: '
	intro = "Who Dares Wins: Who Works Together Wins"

	def __init__(self): #, teamserver):
		Cmd.__init__(self)

	def do_exit(self, arg):
		"Exit SABRE-OC"
		quit()

	def do_list_sessions(self, cmd):
		'Get Running Listeners'
		print('Getting Running Listeners')
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
		except:
			print('No Active Sessions')

	def do_killsession(self, cmd):
		'Kill an existing session: msfconsole1 or empire1 etc..'
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session. all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
			s = input('Enter in session ID: ')
			subprocess.call(['tmux', 'kill-session', '-t', s])
		except:
			print('No Active Sessions')

	def do_sessions(self, cmd):
		'Interact with an existing session: msfconsole1 or empire1 etc..'
		try:
			l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
			li = l.split('\n')
			print('Remember to select a session all you need is the listener ID (msfconsole# or empire#)')
			for i in li:
				print(i)
			s = input('Enter in session ID: ')
			subprocess.call(['tmux', 'attach', '-t', s])
		except:
			print('No Active Sessions')


	def do_msfconsole(self, cmd):
		'Start a MSFCONSOLE Session'
		s = msf(r, '0.0.0.0', 42)
		s.screenMSF()

	def do_external(self, cmd):
		'Start a any External Tool Session'
		t = input('Specify External Tool to run (Empyre, nmap, etc..): ') or 'exit'
		s = external(r, t, 42)
		s.screenEXT()

	def do_ptf(self, cmd):
		'Start a PTF Session'
		s = ptf(r, '0.0.0.0', 42)
		s.screenPTF()

	def do_empire(self, cmd):
		'Start a Empire Session'
		s = empire(r, '0.0.0.0', 42)
		s.screenEmpire()

	def do_listener(self, arg):
		"Go to the listener menu"
		sub_cmd = listeners()
		sub_cmd.cmdloop()

	def do_tpt(self, arg):
		"Go to the TPT menu"
		sub_cmd = TPT()
		sub_cmd.cmdloop()

	def do_operator(self, arg):
		"Go to the operator menu"
		sub_cmd = operator()
		sub_cmd.cmdloop()

	def do_intel(self, arg):
		"Go to the Intel menu"
		sub_cmd = intel()
		sub_cmd.cmdloop()

	def do_auxiliary(self, arg):
		"Go to the Auxiliary Tools Menu"
		sub_cmd = auxiliary()
		sub_cmd.cmdloop()

##### ALIASES #####
	do_interact = do_sessions
	do_list = do_list_sessions

class operator(Cmd):
	prompt = 'OC-Operators: '
	intro = "Who Dares Wins: Who Acts Wins"

	def __init__(self): #, teamserver):
		Cmd.__init__(self)
		#self.ts = teamserver

	def do_exit(self, arg):
		"Exit SABRE-OC"
		quit()

	def do_listener(self, arg):
		"Go to the listener menu"
		sub_cmd = listeners()
		sub_cmd.cmdloop()

	def do_tpt(self, arg):
		"Go to the TPT menu"
		sub_cmd = TPT()
		sub_cmd.cmdloop()

	def do_intel(self, arg):
		"Go to the Intel menu"
		sub_cmd = Intel()
		sub_cmd.cmdloop()

	def do_auxiliary(self, arg):
		"Go to the Auxiliary Tools Menu"
		sub_cmd = auxiliary()
		sub_cmd.cmdloop()

	def do_checkdb(self, arg):
		"Check for connectivity to the DB"
		global r
		value = r.info()
		if value:
			print("Connected!")
		else:
			print("Disconnected")

	def do_list(self, arg):
		"List Available Native Operators (Implants)"
		print("Print Usable Operators (Implants)")
		print('Currently we only have one native implannt')

##### ALIASES #####
	do_operators = do_list

class intel(Cmd):
	prompt = 'OC-Intel: '
	intro = "Who Dares Wins: Who Knows Wins - Under Development"

	def __init__(self): #, teamserver):
		Cmd.__init__(self)
		#self.ts = teamserver

	def do_exit(self, arg):
		"Exit SABRE-OC"
		quit()

	def do_listener(self, arg):
		"Go to the listener menu"
		sub_cmd = listeners()
		sub_cmd.cmdloop()

	def do_tpt(self, arg):
		"Go to the TPT menu"
		sub_cmd = TPT()
		sub_cmd.cmdloop()

	def do_operator(self, arg):
		"Go to the operator menu"
		sub_cmd = operator()
		sub_cmd.cmdloop()

	def do_auxiliary(self, arg):
		"Go to the Auxiliary Tools Menu"
		sub_cmd = auxiliary()
		sub_cmd.cmdloop()

	def do_brief(self, arg):
		"Print Link to Open Source Threat Intel"
		try:
			subprocess.call(['firefox', 'https://otx.alienvault.com/browse/industries/?sort=-created', '&'])
			print('https://otx.alienvault.com/browse/industries/?sort=-created')
		except:
			print('https://otx.alienvault.com/browse/industries/?sort=-created')

	def do_checkdb(self, arg):
		"Check for connectivity to the DB"
		global r
		value = r.info()
		if value:
			print("Connected!")
		else:
			print("Disconnected")

###### ALIASES ######

class auxiliary(Cmd):
	prompt = 'OC-AUX: '
	intro = """Who Dares Wins: Who Has The Best Toys Wins
This is a place holder for adding Auxiliary modules such as Exfil Tools"""

	def __init__(self): #, teamserver):
		Cmd.__init__(self)
		#self.ts = teamserver

	def do_exit(self, arg):
		"Exit SABRE-OC"
		quit()

	def do_listener(self, arg):
		"Go to the listener menu"
		sub_cmd = listeners()
		sub_cmd.cmdloop()

	def do_tpt(self, arg):
		"Go to the TPT menu"
		sub_cmd = TPT()
		sub_cmd.cmdloop()

	def do_operator(self, arg):
		"Go to the operator menu"
		sub_cmd = operator()
		sub_cmd.cmdloop()

	def do_intel(self, arg):
		"Go to the Intel menu"
		sub_cmd = intel()
		sub_cmd.cmdloop()

	def do_syslogdiscover(self, arg):
		"""
Usage: syslogDiscover <PCAP FILE TO PARSE>

This Tool was developed to identify Splunk instances on the network with out network scanning tools such as:
	-nmap
	-zenmap
	-etc...

    This sould be ran with a PCAP file generated filtering only for SYSLOG traffic port 514

    Example: tcpdump -s 65535 -i ens33 port 514 -w syslog-514.pcap

    Author: Aidden Laoch

		"""
		p = input('Specify probable SYSLOG port used [514]: ') or '514'
		cap = input('Specify pcap file to parse [pcap.pcap]: ') or 'pcap.pcap'
		TCP_REVERSE = dict((TCP_SERVICES[k], k) for k in list(TCP_SERVICES.keys()))
		try:
			p = TCP_REVERSE[int(p)]
		except:
			print("Error: That port wasn't in the SCAPY service list")
		try:
			pcapData = readpcap()
			pcapData.parseme(str(cap), p)
		except:
			print("error... try again")

	def do_checkdb(self, arg):
		"Check for connectivity to the DB"
		global r
		value = r.info()
		if value:
			print("Connected!")
		else:
			print("Disconnected")

if __name__ == '__main__':
	os.system('clear')
	r = redis.Redis(
		host='localhost', #Need to add option for changing the teamserver host
		port=6379,)       #Need to add option for changing the teamserver port
	app = HQ()
	app.cmdloop()
