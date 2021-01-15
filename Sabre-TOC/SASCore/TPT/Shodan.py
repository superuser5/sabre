#!/usr/bin/python3

from .settings import r
import subprocess
import time

class shodan():

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

        def screenShodan(self):
                print('Starting shodan CLI in session')
                try:
                        l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
                        li = l.split('\n')
                        n = []
                        for i in li:
                                if 'shodan' in i:
                                        n.append(i.split('shodan')[1])
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
		print('Attempting to start sessions for shodan!')
		time.sleep(2)
		if self.h in l:
			print('already have one')
                        subprocess.call(['/bin/bash', '-c', 'tmux new -s shodan%d "shodan -h && /bin/bash"' % int(nn)])
			print('msfconsole%d' % int(nn))
		else:
                        subprocess.call(["/bin/bash", "-c", "tmux new -s shodan 'shodan -h && /bin/bash'" ])

if __name__ == "__main__":
	#r = redis.Redis(host='localhost', port=6379)
	client = shodan(r, "0.0.0.0", 42)
	client.screenShodan()

