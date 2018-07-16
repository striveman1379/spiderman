from .base import BaseReporter


class BackendReporter(BaseReporter):
    VALID_BACKENDS = []

    def __init__(self, settings, backend_manager):
        super(BackendReporter, self).__init__(settings)
        self._backend = backend_manager.get_backend(self._settings.get('BACKEND'))

        # check backends
        if not BackendReporter._check_backend(self._backend, self.VALID_BACKENDS):
            raise Exception('Invalid backend {0}'.format(self._backend))

        #spider
        self._spider = None

    def start(self, spider):
        self._spider = spider

    def stop(self, reason): pass


    @staticmethod
    def _check_backend(backend, valid_backends):
        for vbackend in valid_backends:
            if isinstance(backend, vbackend): return True
        return False
