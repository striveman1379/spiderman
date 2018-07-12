from .base import BaseRequester
from spiderman.contrib.backends.redis.redis_backend import RedisBackend


class RedisRequester(BaseRequester):
    VALID_BACKENDS = [RedisBackend]

    #default
    _queue_key = 'default'

    def start(self, spider):
        super(RedisRequester, self).start(spider)

        self._queue_key = self._settings.get('QUEUE_KEY')
        return self._backend.start(queue_key=self._queue_key)

    def stop(self, reason):
        super(RedisRequester, self).stop(reason)

        return self._backend.stop(reason)

    def add_requests(self, requests):
        requests = [self.encode_request(r) for r in requests]
        return self._backend.add_requests(requests)

    def get_requests(self, max_requests=0, **kwargs):
        requests = self._backend.get_requests(max_requests, **kwargs)
        if len(requests) > 0:
            requests = [self.decode_request(r) for r in requests]
        return requests
