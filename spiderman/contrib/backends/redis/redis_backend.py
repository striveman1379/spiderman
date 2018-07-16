from spiderman.contrib.backends.backend import BaseBackend
from . import connection


class RedisBackend(BaseBackend):
    _server = None

    # base funcs
    def __init__(self, settings):
        self._settings = settings

    def start(self):
        if self.is_running():
            return

        super(RedisBackend, self).start()

        # _server
        self._server = connection.from_settings(self._settings)
        self._server.ping()

    def stop(self, reason):
        if not self.is_running():
            return
        self._server = None
        super(RedisBackend, self).stop(reason)

    # redis _server funcs
    def save(self):
        if self._server is None:
            return
        self._server.save()

    def execute_command(self, *args, **options):
        if self._server is None: return
        return self._server.execute_command(*args, **options)