from __future__ import absolute_import

from collections import deque
from scrapy.core.scheduler import Scheduler
from spiderman.core.managers import SpidermanManager
from spiderman.settings import ScrapySettingsAdapter



class SpidermanScheduler(Scheduler):
    def __init__(self, crawler):
        self._crawler = crawler
        self._pending_requests = deque()
        self._manager = SpidermanManager(ScrapySettingsAdapter(crawler.settings))

        # settings
        self._max_next_requests = crawler.settings.get('MAX_NEXT_REQUETS', 1)

    def __len__(self):
        return len(self._pending_requests)

    @property
    def crawler(self): return self._crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        self._manager.start(spider)

    def close(self, reason):
        self._manager.stop(reason)

    def enqueue_request(self, request):
        self._manager.add_requests([request])

    def next_request(self):
        requests = self._manager.get_requests(self._max_next_requests)
        if len(requests) > 0:
            self._pending_requests.extend(requests)
        return self._pending_requests.popleft() if self._pending_requests else None

