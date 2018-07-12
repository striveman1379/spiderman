import six
import redis
from scrapy.utils.misc import load_object

from . import defaults


# Shortcut maps 'setting name' -> 'parmater name'.
SETTINGS_PARAMS_MAP = {
    'URL': 'url',
    'HOST': 'host',
    'PORT': 'port',
    'ENCODING': 'encoding',
    'SOCKET_TIMEOUT': 'socket_timeout',
    'SOCKET_CONNECT_TIMEOUT': 'socket_connect_timeout',
    'RETRY_ON_TIMEOUT': 'retry_on_timeout',
}


def get_redis_from_settings(settings):
    """Returns a redis client instance from given Scrapy settings object.

    This function uses ``get_client`` to instantiate the client and uses
    ``defaults.REDIS_PARAMS`` global as defaults values for the parameters. You
    can override them using the ``REDIS_PARAMS`` setting.

    Parameters
    ----------
    settings : Settings
        A scrapy settings object. See the supported settings below.

    Returns
    -------
    server
        Redis client instance.

    Other Parameters
    ----------------
    REDIS_URL : str, optional
        Server connection URL.
    REDIS_HOST : str, optional
        Server host.
    REDIS_PORT : str, optional
        Server port.
    REDIS_ENCODING : str, optional
        Data encoding.
    REDIS_PARAMS : dict, optional
        Additional client parameters.

    """

    params = {
        'encoding':'utf-8',
        'redis_cls':redis.StrictRedis,
    }
    params.update(settings.get('PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])

    return get_redis(**params)


# Backwards compatible alias.
from_settings = get_redis_from_settings


def get_redis(**kwargs):
    """Returns a redis client instance.

    Parameters
    ----------
    redis_cls : class, optional
        Defaults to ``redis.StrictRedis``.
    url : str, optional
        If given, ``redis_cls.from_url`` is used to instantiate the class.
    **kwargs
        Extra parameters to be passed to the ``redis_cls`` class.

    Returns
    -------
    server
        Redis client instance.

    """
    redis_cls = redis.StrictRedis
    url = kwargs.pop('url', None)
    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)
