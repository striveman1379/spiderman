from __future__ import absolute_import
from .base import BaseMiddleware

class SpiderMiddleware(BaseMiddleware):
    def process_spider_output(self, response, result, spider):
        return self.scheduler.process_spider_output(response, result, spider)