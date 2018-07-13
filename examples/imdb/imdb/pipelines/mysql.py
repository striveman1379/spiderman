
from spiderman.contrib.pipelines import BackendPipeline


class MysqlPipeline(BackendPipeline):

    BACKEND = 'mysql'

    def process_item(self, item, spider):
        self._backend.insert(self, "top250", item)

