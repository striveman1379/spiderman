

class BaseReporter(object):

    def __init__(self, settings):
        self._settings = settings

    def on_receive_requests(self, requests):
        pass

    def on_process_page(self):
        pass

    def on_download_exception(self, request, exception, spider):
        pass

    def on_spider_exception(self, response, exception, spider):
        pass

    def on_spider_error(self, failure, response, spider):
        pass