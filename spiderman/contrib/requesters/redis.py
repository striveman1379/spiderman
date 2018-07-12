from .base import BaseRequester
from spiderman.contrib.backends.redis.redis_backend import RedisBackend


class RedisRequester(BaseRequester):
    VALID_BACKENDS = [RedisBackend]

    #default
    _queue_key = 'default'
    _queue_cls = 'queue'

    def start(self):
        self._queue_key = self._settings.get('QUEUE_KEY')
        self._queue_cls = self._settings.get('QUEUE_CLASS')
        return self._backend.start( queue_key=self._queue_key, queue_cls=self._queue_cls)

    def stop(self, reason):
        return self._backend.stop(reason)

    def add_requests(self, requests):
        return self._backend.add_requests(requests)

    def get_requests(self, max_requests=0, **kwargs):
        return self._backend.get_requests(self, max_requests, **kwargs)