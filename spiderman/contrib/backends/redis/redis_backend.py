from spiderman.contrib.backends.backend import BaseBackend
from . import connection, picklecompat
from scrapy.utils.misc import load_object


class RedisBackend(BaseBackend):
    def __init__(self, settings):
        self._settings = settings
        self._request_timeout = settings.get('REQUEST_TIMEOUT')
        self.queue=None

    def __len__(self):
        return len(self.queue)

    def start(self, queue_key, queue_cls):
        if self.is_started():
            return

        super(RedisBackend, self).start()

        # server
        self.server = connection.from_settings(self._settings)
        self.server.ping()

        # queue
        self.queue = load_object(queue_cls)(
            server=self.server,
            key=queue_key,
            serializer=picklecompat,
        )

    def stop(self, reason):
        self.queue.clear()
        super(RedisBackend, self).stop(reason)

    def add_requests(self, requests):
        for r in requests:
            self.queue.push(r)
        return True

    def get_requests(self, max_requests=0, **kwargs):
        request = self.queue.pop(self._request_timeout)

        return [request] if request is not None else []