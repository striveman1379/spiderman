from __future__ import absolute_import
from scrapy.utils.misc import load_object


class ReporterManager(object):

    def __init__(self, settings, backend_manager):
        self._settings = settings
        self._reporter = load_object(settings.get('MODULE'))(settings, backend_manager)

    def start(self, spider):
        return self._reporter.start(spider)

    def stop(self):
        return self._reporter.stop()

    def on_receive_requests(self, requests):
        self._reporter.on_receive_requests(requests)

    def on_process_page(self, request):
        self._reporter.on_process_page(request)

    def on_download_exception(self, request, exception, spider):
        self._reporter.on_download_exception(request, exception, spider)

    def on_spider_exception(self, response, exception, spider):
        self._reporter.on_download_exception(response, exception, spider)

    def on_spider_error(self, failure, response, spider):
        self._reporter.on_spider_error(failure, response, spider)