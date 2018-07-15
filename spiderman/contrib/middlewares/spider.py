from __future__ import absolute_import
from .base import BaseMiddleware

class SpiderMiddleware(BaseMiddleware):

    def process_spider_exception(self, response, exception, spider):
        return self.scheduler.process_spider_exception(response, exception, spider)