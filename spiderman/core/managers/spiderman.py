from __future__ import absolute_import
from scrapy.utils.misc import load_object
from .backends import BackendManager
from .requester import RequesterManager


class SpidermanManager(object):
    def __init__(self, settings):
        # setiings
        self._settings = settings

        # init backend manager
        self._backend_manager = BackendManager(settings.get('BACKENDS'))

        # get requester
        self._requester_manager = RequesterManager(settings.get('REQUESTER'), self._backend_manager)

        #spider
        self._spider = None

    @property
    def settings(self): return self._settings

    @property
    def backend_manager(self): return self._backend_manager

    @property
    def requester_manager(self): return self._requester_manager

    def start(self, spider):
        self._spider = spider
        self._backend_manager.start()
        self._requester_manager.start(spider)

    def stop(self, reason):
        self._requester_manager.stop(reason)
        self._backend_manager.stop(reason)

    def add_requests(self, requests):
        return self._requester_manager.add_requests(requests)

    def get_requests(self, max_requests=0, **kwargs):
        return self._requester_manager.get_requests(max_requests, **kwargs)

    def process_spider_output(self, response, result, spider):
        return result



    def request_error(self, request, error):
        pass

    def finished(self):
        pass