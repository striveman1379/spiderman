from __future__ import absolute_import

from .redis import RedisBackend



def create_backend(settings):
    from scrapy.utils.misc import load_object
    backend_settings = settings.get('BACKENDS')
    backend = load_object(backend_settings['MODULE'])(backend_settings)
    return backend