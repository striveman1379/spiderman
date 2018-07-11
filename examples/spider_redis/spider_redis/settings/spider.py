

BACKENDS = {
    'MODULE': 'spiderman.contrib.backends.RedisBackend',
    'URL': None,
    'HOST': 'localhost',
    'PORT': 6379,
    'ENCODING': 'utf-8',
    'QUEUE_KEY': '%(spider)s:requests',
    'QUEUE_CLASS': 'spiderman.contrib.backends.redis.queue.FifoQueue',
    'REQUEST_TIMEOUT': 3,

    # Sane connection defaults.
    'PARAMS': {
        'socket_timeout': 30,
        'socket_connect_timeout': 30,
        'retry_on_timeout': True,
    }
}