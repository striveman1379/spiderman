from __future__ import absolute_import
from scrapy.utils.misc import load_object



class BackendManager(object):
    def __init__(self, settings):
        self._settings = settings
        self._backends = {}

        # init all backends
        for name, backend_setting in settings.items():
            self._backends[name] = load_object(backend_setting['MODULE'])(backend_setting)


    def get_backend(self, name): return self._backends.get(name, None)
