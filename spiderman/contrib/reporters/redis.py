import traceback
from .backed import BackendReporter
from spiderman.contrib.backends.redis.redis_backend import RedisBackend


class RedisReporter(BackendReporter):
    VALID_BACKENDS = [RedisBackend]

    _reporter_prefix = 'reporter'

    def start(self, spider):
        super(RedisReporter, self).start(spider)
        self._reporter_prefix = self._settings.get('REPORTER_PREFIX')
        # connect redis server
        self._backend.start()
        return

    def stop(self, reason):
        super(RedisReporter, self).stop(reason)
        return self._backend.stop(reason)

    def on_receive_requests(self, requests):
        for r in requests:
            key = self._reporter_prefix + r.url
            self._backend.execute_command("HMSET", key,
                                          'status', 'on_receive_requests',
                                          'exception', 'None'
                                          'spider_id', str(self._spider.id)
                                          )

    def on_download_exception(self, request, exception, spider):
        key = self._reporter_prefix + request.url
        print('=='*50)
        print(key)
        print(spider.id)
        print(str(traceback.format_exc()))
        self._backend.execute_command("HMSET", key,
                                      'spider_id', spider.id,
                                      'status', 'on_download_exception',
                                      #'exception', str(traceback.format_exc())
                                      )

    def on_spider_exception(self, response, exception, spider):
        key = self._reporter_prefix + response.url
        self._backend.execute_command("HMSET", key,
                                      'spider_id', spider.id,
                                      'status', 'on_spider_exception',
                                      'exception', str(traceback.format_exc())
                                      )

    def on_spider_error(self, failure, response, spider):
        key = self._reporter_prefix + response.url
        self._backend.execute_command("HMSET", key,
                                      'spider_id', spider.id,
                                      'status', 'on_spider_error',
                                      'exception', str(failure)
                                      )

    def on_item_scraped(self, item, response, spider):
        key = self._reporter_prefix + response.url
        self._backend.execute_command("HMSET", key,
                                      'spider_id', spider.id,
                                      'status', 'on_item_scraped',
                                      )
