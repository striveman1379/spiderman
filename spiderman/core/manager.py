from __future__ import absolute_import
from spiderman.contrib.backends import create_backend




class SpidermanManager(object):
    def __init__(self, settings):
        self._settings = settings

        # backend
        self._backend = create_backend(settings)

    @property
    def settings(self): return self._settings

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