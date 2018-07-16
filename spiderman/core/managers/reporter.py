from __future__ import absolute_import
from scrapy.utils.misc import load_object



class ReporterManager(object):

    def __init__(self, settings):
        self._settings = settings
        self._reporter = load_object(settings.get('MODULE'))(settings)


    def start(self): pass


    def stop(self): pass


    def on_receive_requests(self, requests):
        self._reporter.on_receive_requests(requests)


    def on_process_page(self):
        self._reporter.on_process_page()


    def on_download_exception(self, request, exception, spider):
        self._reporter.on_download_exception(request, exception, spider)

    def on_spider_exception(self, response, exception, spider):
        self._reporter.on_download_exception(response, exception, spider)

    def on_spider_error(self, failure, response, spider):
        self._reporter.on_spider_error(failure, response, spider)