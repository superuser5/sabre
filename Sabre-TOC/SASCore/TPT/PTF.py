#!/usr/bin/python

import subprocess
from settings import r

class ptf():

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

        def screenPTF(self):
                print 'Starting the "PenTest Framework" in session'
                try:
                        l = subprocess.check_output(['tmux', 'list-sessions'], shell=False)
                        li = l.split('\n')
                        n = []
                        for i in li:
                                if 'ptf' in i:
                                        n.append(i.split('ptf')[1])
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
                if 'ptf' in l:
                        print '''
ERROR! Already have one!:
'''
                        subprocess.call(["/bin/bash", "-c", "tmux new -s ptf%d 'clear && cd /root/ptf && ./ptf'" % int(nn)])
                        print 'ptf%d' % int(nn)
                else:
                        subprocess.call(["/bin/bash", "-c", "tmux new -s ptf 'clear && cd /root/ptf && ./ptf'"])


if __name__ == "__main__":
        #r = redis.Redis(host='localhost', port=6379)
        client = ptf(r, "0.0.0.0", 42)
        client.screenPTF()
