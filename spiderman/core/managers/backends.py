from __future__ import absolute_import
from scrapy.utils.misc import load_object


class BackendManager(object):
    def __init__(self, settings):
        self._settings = settings
        self._backends = {}

    def open(self, name):
        backend = self.get_backend(name)
        backend.start()
        return backend

    def close(self, name):
        backend = self._backends.get(name, None)
        if backend is None: return
        backend.stop()
        del self._backends[name]

    def start(self): pass

    def stop(self, reason=None):
        for name, backend in self._backends.items():
            backend.stop(reason)
        self._backends = {}

    def get_backend(self, name):
        backend = self._backends.get(name, None)
        if backend is None:
            backend = self._create_backend(name)
            self._backends[name] = backend

        return backend

    def _create_backend(self, name):
        backend_setting = self._settings.get(name, None)
        if backend_setting is None:
            raise Exception('can not find backend {0}'.format(name))

        return load_object(backend_setting['MODULE'])(backend_setting)
