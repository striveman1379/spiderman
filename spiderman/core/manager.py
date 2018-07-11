from __future__ import absolute_import




class SpidermanManager(object):
    def __init__(self, settings):
        self._settings = settings

    @property
    def settings(self): return self._settings

    def start(self):
        pass

    def stop(self):
        pass

    def add_requests(self, requests):
        pass

    def get_next_requests(self, max_next_requests=0, **kwargs):
        pass

    def page_crawled(self, response):
        pass

    def links_extracted(self, request, links):
        pass

    def request_error(self, request, error):
        pass

    def finished(self):
        pass