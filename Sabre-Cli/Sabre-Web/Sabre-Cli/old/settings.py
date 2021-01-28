import redis

config = {
	'host': '192.168.172.130',
	'port': 6379,
	'db': 0,
}

r = redis.StrictRedis(**config)
