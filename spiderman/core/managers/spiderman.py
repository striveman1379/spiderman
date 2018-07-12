from __future__ import absolute_import
from .backends import BackendManager



class SpidermanManager(object):
    def __init__(self, settings):
        self._settings = settings

        # init backend manager
        self._backend_manager = BackendManager(settings.get('BACKENDS'))

        # get backend
        self._backend = self._backend_manager.get_backend(settings.get('SPIDER_MANAGER_BACKEND'))

    @property
    def settings(self): return self._settings

    @property
    def backend_manager(self): return self._backend_manager

    def start(self, spider):
        self._backend.open(spider)

    def stop(self, reason):
        self._backend.close(reason)

    def add_requests(self, requests):
        return self._backend.add_requests(requests)

    def get_requests(self, max_requests=0, **kwargs):
        return self._backend.get_requests(max_requests, **kwargs)

    def page_crawled(self, response):
        pass

    def links_extracted(self, request, links):
        pass

    def request_error(self, request, error):
        pass

    def finished(self):
        pass