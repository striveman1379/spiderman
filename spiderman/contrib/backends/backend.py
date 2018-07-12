class BaseBackend(object):
    _is_started = False

    def start(self):
        self._is_started = True

    def stop(self, reason):
        self._is_started = False

    def is_started(self):
        return self._is_started
