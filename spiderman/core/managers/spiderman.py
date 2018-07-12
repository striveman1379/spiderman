from __future__ import absolute_import
from scrapy.utils.misc import load_object
from .backends import BackendManager



class SpidermanManager(object):
    def __init__(self, settings):
        self._settings = settings

        # init backend manager
        self._requester_manager = BackendManager(settings.get('BACKENDS'))

        # get requester
        requester_setting = settings.get('REQUESTER')
        self._requester = load_object(requester_setting.get('MODULE'))(requester_setting, self._requester_manager)

    @property
    def settings(self): return self._settings

    @property
    def backend_manager(self): return self._requester_manager

    def start(self, spider):
        self._requester.start(spider)

    def stop(self, reason):
        self._requester.stop(reason)

    def add_requests(self, requests):
        return self._requester.add_requests(requests)

    def get_requests(self, max_requests=0, **kwargs):
        return self._requester.get_requests(max_requests, **kwargs)

    def page_crawled(self, response):
        pass

    def links_extracted(self, request, links):
        pass

    def request_error(self, request, error):
        pass

    def finished(self):
        pass