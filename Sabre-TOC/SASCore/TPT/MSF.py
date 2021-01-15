#!/usr/bin/python3

from .settings import r
import subprocess
import time

class msf():

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

        def screenMSF(self):
                print('Starting the msfconsole in session')
                try:
                        l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
                        li = l.split('\n')
                        n = []
                        for i in li:
                                if 'msfconsole' in i:
                                        n.append(i.split('msfconsole')[1])
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
		if 'msfconsole' in l:
			print('already have one')
			#subprocess.call(['screen', '-S', 'msfconsole%d' % int(nn), '-s', 'msfconsole'])
                        subprocess.call(['/bin/bash', '-c', 'tmux new -s msfconsole%d /opt/Sabre-TOC/SASCore/TPT/msf-cli.py' % int(nn)])
			print('msfconsole%d' % int(nn))
		else:
			#subprocess.call(['screen', '-S', 'msfconsole', '-s', 'msfconsole'])
                        subprocess.call(["/bin/bash", "-c", "tmux new -s msfconsole /opt/Sabre-TOC/SASCore/TPT/msf-cli.py"])

if __name__ == "__main__":
	#r = redis.Redis(host='localhost', port=6379)
	client = msf(r, "0.0.0.0", 42)
	client.screenMSF()

