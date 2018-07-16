

class BaseReporter(object):
    def __init__(self, settings, *args, **kwargs):
        self._settings = settings

    def start(self, *args, **kwargs): pass

    def stop(self, *args, **kwargs): pass

    def on_receive_requests(self, requests):
        pass

    def on_download_exception(self, request, exception, spider):
        pass

    def on_spider_exception(self, response, exception, spider):
        pass

    def on_spider_error(self, failure, response, spider):
        pass

    def on_item_scraped(self, item, response, spider):
        pass

    def on_item_dropped(self, item, spider, exception):
        pass