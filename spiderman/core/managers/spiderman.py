from __future__ import absolute_import
from scrapy.utils.misc import load_object
from .backends import BackendManager
from .requester import RequesterManager
from .reporter import ReporterManager


class SpidermanManager(object):
    def __init__(self, settings):
        # setiings
        self._settings = settings

        # backend manager
        self._backend_manager = BackendManager(settings.get('BACKENDS'))

        #  requester manager
        self._requester_manager = RequesterManager(settings.get('REQUESTER'), self._backend_manager)

        # reporter manager
        self._reporter_manager = ReporterManager(settings.get('REPORTER'))

        #spider
        self._spider = None

    @property
    def settings(self): return self._settings

    @property
    def backend_manager(self): return self._backend_manager

    @property
    def requester_manager(self): return self._requester_manager

    def start(self, spider):
        # init spider
        self._spider = self._init_spider(spider)


        # start manager
        self._backend_manager.start()
        self._requester_manager.start(spider)
        self._reporter_manager.start()

    def stop(self, reason):
        self._requester_manager.stop(reason)
        self._backend_manager.stop(reason)

    def add_requests(self, requests):
        return self._requester_manager.add_requests(requests)

    def get_requests(self, max_requests=0, **kwargs):
        requests = self._requester_manager.get_requests(max_requests, **kwargs)
        if len(requests) > 0:
            self._reporter_manager.on_receive_requests(requests)
        return requests


    def process_download_exception(self, request, exception, spider):
        return self._reporter_manager.on_download_exception(request, exception, spider)

    def process_spider_exception(self, response, exception, spider):
        return self._reporter_manager.on_spider_exception(response, exception, spider)

    def process_spider_error(self, failure, response, spider):
        return self._reporter_manager.on_spider_error(failure, response, spider)


    def _init_spider(self, spider):
        id = self._settings.get('SPIDER_ID')
        if id is None:
            id = 'default'
        setattr(spider, 'id', id)
        return spider