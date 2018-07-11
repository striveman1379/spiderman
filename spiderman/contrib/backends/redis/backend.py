import importlib
import six

from spiderman.contrib.backends.base import BaseBackend
from . import connection, defaults
from scrapy.utils.misc import load_object

class RedisBackend(BaseBackend):
    def __init__(self, server,
                 queue_key=defaults.SCHEDULER_QUEUE_KEY,
                 queue_cls=defaults.SCHEDULER_QUEUE_CLASS,
                 serializer=None):

        self.server = server
        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.serializer = serializer

    def __len__(self):
        return len(self.queue)

    def open(self, spider, settings):
        # spider
        self.spider = spider

        # server
        self.server = connection.from_settings(settings)
        self.server.ping()

        # queue
        self.queue = load_object(self.queue_cls)(
            server=self.server,
            spider=spider,
            key=self.queue_key % {'spider': spider.name},
            serializer=self.serializer,
        )

    def close(self, reason):
        self.queue.clear()

    def enqueue_request(self, request):
        self.queue.push(request)
        return True

    def next_request(self):
        block_pop_timeout = self.idle_before_close
        request = self.queue.pop(block_pop_timeout)
        return request