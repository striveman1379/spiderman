from spiderman.contrib.backends.backend import BaseBackend
from . import connection
from scrapy.utils.misc import load_object
from .container import FifoQueue, UnsortedSet


class RedisBackend(BaseBackend):
    server = None
    container = None
    deduplicate_key = 'default_deduplicate'

    def __init__(self, settings):
        self._settings = settings
        self._request_timeout = settings.get('REQUEST_TIMEOUT')
        self.container = None

    def __len__(self):
        if self.container is None:
            return -1
        return len(self.container)

    def start(self, container_key):
        if self.is_running():
            return

        super(RedisBackend, self).start()

        # server
        self.server = connection.from_settings(self._settings)
        self.server.ping()

        # container
        self.container = UnsortedSet(server=self.server, key=container_key)

        # deduplicate
        self.deduplicate_key = container_key + '_deduplicate'

    def stop(self, reason):
        if not self.is_running():
            return
        self.server = None
        super(RedisBackend, self).stop(reason)

    def add_requests(self, requests):
        if self.container is None:
            return False
        for r in requests:
            self.container.push(r)
        return True

    def get_requests(self, max_requests=0, **kwargs):
        if self.container is None:
            return []
        request = self.container.pop(self._request_timeout)

        return [request] if request is not None else []

    def clear(self):
        if self.container:
            self.container.clear()

    def execute_command(self, *args, **options):
        if self.server is None: return
        self.server.execute_command(self, *args, **options)

    def set_flag(self, flag):
        return self.server.sadd(self.deduplicate_key, flag) == 1
