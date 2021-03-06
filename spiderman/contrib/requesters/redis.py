from .base import BaseRequester
from spiderman.contrib.backends.redis.redis_backend import RedisBackend
from pickle import dumps

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
        p = self._backend.pipeline()
        if p is None:
            return

        # deduplicate
        for r in requests:
            value = r.url + str(r.body)
            p.execute_command("SADD", self._deduplicater_key, value)
        results = p.execute()

        request_list = []
        # loop
        for i, r in enumerate(requests):
            if results[i] == 1:
                p.execute_command("LPUSH", self._container_key, self.encode_request(r))
        p.execute()

    def get_requests(self, max_requests=0, **kwargs):
        p = self._backend.pipeline()
        if p is None:
            return

        for i in range(max(1,max_requests)):
            if self._request_timeout > 0:
                p.execute_command("BRPOP", self._container_key, self._request_timeout)
            else:
                p.execute_command("RPOP", self._container_key)

        result = p.execute()

        requests = []
        for data in result:
            if data is None:
                continue
            if isinstance(data, tuple):
                requests.append(self.decode_request(data[1]))
            else:
                requests.append(self.decode_request(data))
        return requests
