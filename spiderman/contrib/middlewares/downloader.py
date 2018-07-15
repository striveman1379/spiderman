from __future__ import absolute_import
from .base import BaseMiddleware

class DownloaderMiddleware(BaseMiddleware):
    def process_exception(self, request, exception, spider):
        return self.scheduler.process_download_exception(request, exception, spider)