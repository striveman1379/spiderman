from .base import BaseRequester
from spiderman.contrib.backends.redis.redis_backend import RedisBackend


class RedisRequester(BaseRequester):
    VALID_BACKENDS = [RedisBackend]

    #default
    _container_key = 'requester'
    _deduplicater_key = "requester_deduplicate"
    _request_timeout = 0

    def start(self, spider):
        super(RedisRequester, self).start(spider)

        # read settings
        self._request_timeout = self._settings.get('REQUEST_TIMEOUT')
        self._container_key = self._settings.get('CONTAINER_KEY')
        self._deduplicater_key = self._settings.get('DEDUPLICATER_KEY')

        # connect redis server
        self._backend.start()
        return

    def stop(self, reason):
        super(RedisRequester, self).stop(reason)
        return self._backend.stop(reason)

    def add_requests(self, requests):
        for r in requests:
            if self._backend.execute_command("SADD", self._deduplicater_key, r.url) == 1:
                self._backend.execute_command("LPUSH", self._container_key, self.encode_request(r))

    def get_requests(self, max_requests=0, **kwargs):
        data = None
        if self._request_timeout > 0:
            data = self._backend.execute_command("BRPOP", self._container_key, self._request_timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self._backend.execute_command("RPOP", self._container_key)

        if data is None:
            return []
        else:
            return [self.decode_request(data)]
