#!/usr/bin/python3

import subprocess
from .settings import r

class empire():

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

	def screenEmpire(self):
		print('Starting the empire in session')
		try:
			l = subprocess.check_output(['tmux', 'list-session'], shell=False)
			li = l.split('\n')
			n = []
			for i in li:
				if 'empire' in i:
					n.append(i.split('empire')[1])
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
		if 'empire' in l:
			print('''
ERROR! Already have one!:
''')
			print('Due to empire behaving badly with more then run instence running at a time, We will have to share the current existing session already running. Teampire is in the works so hopefully this wont be an issue for long.')
		else:
			subprocess.call(['/bin/bash', '-c', 'tmux new -s empire "clear && cd /pentest/post-exploitation/empire-py/ && empire"'])


if __name__ == "__main__":
	#r = redis.Redis(host='localhost', port=6379)
	client = listener(r, "0.0.0.0", 42)
	client.screenEmpire()
