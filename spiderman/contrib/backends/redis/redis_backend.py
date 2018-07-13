from spiderman.contrib.backends.backend import BaseBackend
from . import connection
from scrapy.utils.misc import load_object
from .queue import FifoQueue


class RedisBackend(BaseBackend):
    server = None
    queue = None

    def __init__(self, settings):
        self._settings = settings
        self._request_timeout = settings.get('REQUEST_TIMEOUT')
        self.queue = None

    def __len__(self):
        if self.queue is None:
            return -1
        return len(self.queue)

    def start(self, queue_key):
        if self.is_running():
            return

        super(RedisBackend, self).start()

        # server
        self.server = connection.from_settings(self._settings)
        self.server.ping()

        # queue
        self.queue = FifoQueue(server=self.server, key=queue_key)

    def stop(self, reason):
        if not self.is_running():
            return
        self.server.shutdown()
        self.server = None
        super(RedisBackend, self).stop(reason)

    def add_requests(self, requests):
        if self.queue is None:
            return False
        for r in requests:
            self.queue.push(r)
        return True

    def get_requests(self, max_requests=0, **kwargs):
        if self.queue is None:
            return []
        request = self.queue.pop(self._request_timeout)

        return [request] if request is not None else []

    def clear(self):
        if self.queue:
            self.queue.clear()

    def execute_command(self, *args, **options):
        if self.server is None: return
        self.server.execute_command(self, *args, **options)
