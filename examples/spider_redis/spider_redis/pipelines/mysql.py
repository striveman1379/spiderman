


class MysqlPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        backend = spider.crawler.engine.slot.scheduler.manager.backend_manager

