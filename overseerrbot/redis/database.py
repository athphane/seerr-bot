from redis import Redis

from overseerrbot import config


class RedisDatabase:
    def __init__(self):
        self.redis = Redis(
            host=config.get('redis', 'host'),
            port=config.get('redis', 'port'),
            password=config.get('redis', 'password'),
            decode_responses=True
        )

    def clearDatabase(self):
        self.redis.flushall()

    def checkIfSent(self, request_id):
        print('Checking if sent...')
        return self.redis.get(request_id) == '1'

    def markAsSent(self, request_id):
        print('Marking as sent...')
        self.redis.set(request_id, '1')
