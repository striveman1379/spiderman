from __future__ import absolute_import

from collections import deque
from scrapy.core.scheduler import Scheduler
from spiderman.core.manager import SpidermanManager
from spiderman.settings import ScrapySettingsAdapter



class SpidermanScheduler(Scheduler):
    def __init__(self, crawler):
        self.crawler = crawler
        self._pending_requests = deque()
        self._manager = SpidermanManager(ScrapySettingsAdapter(crawler.settings))

    def __len__(self):
        return len(self._pending_requests)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        pass

    def close(self, reason):
        pass

    def enqueue_request(self, request):
        self._manager.add_requests([request])

    def next_request(self):
        return self._pending_requests.popleft() if self._pending_requests else None

