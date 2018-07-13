from __future__ import absolute_import


class BackendPipeline(object):

    BACKEND = None

    @property
    def backend(self): return self._backend

    def open_spider(self, spider):
        if self.BACKEND is None: raise NotImplementedError('BACKEND attribute must be assigned')
        backend_manager = spider.crawler.engine.slot.scheduler.manager.backend_manager
        self._backend = backend_manager.open(self.BACKEND)

    def close_spider(self, spider):
        if self._backend is None: return
        self._backend.close()



