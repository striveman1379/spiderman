import importlib
import six

from spiderman.contrib.backends.backend import BaseBackend
from . import connection, defaults, picklecompat
from scrapy.utils.misc import load_object

class RedisBackend(BaseBackend):
    def __init__(self, settings):
        self._settings = settings
        self._queue_key = settings.get('QUEUE_KEY')
        self._queue_cls = settings.get('QUEUE_CLASS')
        self._request_timeout = settings.get('REQUEST_TIMEOUT')
        self._serializer = picklecompat

    def __len__(self):
        return len(self.queue)

    def open(self, spider):
        # spider
        self.spider = spider

        # server
        self.server = connection.from_settings(self._settings)
        self.server.ping()

        # queue
        self.queue = load_object(self._queue_cls)(
            server=self.server,
            spider=spider,
            key=self._queue_key % {'spider': spider.name},
            serializer=self._serializer,
        )

    def close(self, reason):
        self.queue.clear()

    def add_requests(self, requests):
        for r in requests:
            self.queue.push(r)
        return True

    def get_requests(self, max_requests=0, **kwargs):
        request = self.queue.pop(self._request_timeout)

        return [request] if request is not None else []