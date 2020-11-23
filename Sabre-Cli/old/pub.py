#!/usr/bin/python
import os
import redis
import sys


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
    name = os.environ['sabreS']
    channel = os.environ['sabreT']

    print 'Welcome to {channel}'.format(**locals())

    while True:
        message = raw_input('Enter a message: ')

        if message.lower() == 'exit':
            break

        message = '{name} says: {message}'.format(**locals())

        r.publish(channel, message)
