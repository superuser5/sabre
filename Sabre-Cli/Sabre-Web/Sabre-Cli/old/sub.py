#!/usr/bin/python

import redis
import sys
import notify2
import os

if __name__ == '__main__':
    h = os.environ['TOC']
    p = os.environ['TOCP']
    passme = os.environ['sabreP']
    config = {
        'host': h,
        'port': p,
        'db': 0,
        'password' : passme,
    }

    r = redis.StrictRedis(**config)
    channel = os.environ['sabreT']


    notify2.init("SABRE")
    pubsub = r.pubsub()
    pubsub.subscribe(channel)

    print 'Listening to {channel}'.format(**locals())

    while True:
        for item in pubsub.listen():
		type(item['data'])
        	n = notify2.Notification("Message: ", str(item['data']), 'notification-message-im')
        	n.show()
        	print item['data']
