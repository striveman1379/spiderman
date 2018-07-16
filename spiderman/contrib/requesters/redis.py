from .base import BaseRequester
from spiderman.contrib.backends.redis.redis_backend import RedisBackend


class RedisRequester(BaseRequester):
    VALID_BACKENDS = [RedisBackend]

    #default
    _container_key = 'default'

    def start(self, spider):
        super(RedisRequester, self).start(spider)

        self._container_key = self._settings.get('CONTAINER_KEY')
        return self._backend.start(container_key=self._container_key)

    def stop(self, reason):
        super(RedisRequester, self).stop(reason)

        return self._backend.stop(reason)

    def add_requests(self, requests):
        request_list = []
        for r in requests:
            if self._backend.set_flag(r.url):
                request_list.append(self.encode_request(r))
            # else:
            #   print('add deduplicate request >> ', r.url)
        return self._backend.add_requests(request_list)

    def get_requests(self, max_requests=0, **kwargs):
        requests = self._backend.get_requests(max_requests, **kwargs)
        if len(requests) > 0:
            requests = [self.decode_request(r) for r in requests]
        return requests
