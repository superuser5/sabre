#!/usr/bin/python3

import pexpect
from screenutils import list_screens, Screen
import socket

class screenit():

	def __init__(self):
		self.child = ''
	
	def screenstart(self):
		host = socket.gethostname()
		child = pexpect.spawn('screen')
		#child.sendcontrol('a');
		#child.send('c');
		child.send(' ');
		child.send("ls");
		child.expect('@%s' % host);
		print(child.before)
		print('@%s' % host);

	def screenutil(self):
		host = socket.gethostname()
		list_screens()
		s = Screen('session1', True)
		s.send_commands('bash')
		s.send_commands('ls')
		s.enable_logs()
		s.send_commands("df")
		s.expect('\@%s' % host)
		print(s.before)
		print next(s.logs)

if __name__ == "__main__":
	inst = screenit()
	inst.screenstart()
