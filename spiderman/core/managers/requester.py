from __future__ import absolute_import
from scrapy.utils.misc import load_object


class RequesterManager(object):
    def __init__(self, settings, backend_manager):
        self._settings = settings
        self._requester = load_object(settings.get('MODULE'))(settings, backend_manager)

    def start(self, spider):
        return self._requester.start(spider)

    def stop(self, reason=None):
        return self._requester.stop(reason)


    def add_requests(self, requests):
        return self._requester.add_requests(requests)

    def get_requests(self, max_requests=0, **kwargs):
        return self._requester.get_requests(max_requests, **kwargs)

