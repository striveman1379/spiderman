



class BaseRequester(object):

    VALID_BACKENDS = []

    def __init__(self, settings, backend_manager):
        self._settings = settings
        self._backend = backend_manager.get(self._settings.get('BACKEND'))

        # check backends
        if not BaseRequester._check_backend(self._backend, self.VALID_BACKENDS):
            raise Exception('Invalid backend {0}'.format(self._backend))


    def start(self): pass

    def stop(self, reason): pass

    def add_requests(self, requests): raise NotImplementedError('add_requests must be implemented')

    def get_requests(self, max_requests=0, **kwargs): raise NotImplementedError('get_requests must be implemented')


    @staticmethod
    def _check_backend(backend, valid_backends):
        for vbackend in valid_backends:
            if isinstance(backend, vbackend): return True
        return False