

BACKENDS = {
    'redis':
    {
        'MODULE': 'spiderman.contrib.backends.RedisBackend',
        'URL': None,
        'HOST': 'localhost',
        'PORT': 6379,
        'REQUEST_TIMEOUT': 3,

        'SOCKET_TIMEOUT': 30,
        'SOCKET_CONNECT_TIMEOUT': 30,
        'RETRY_ON_TIMEOUT': True,
    },
    'mysql':
    {
        'MODULE': 'spiderman.contrib.backends.MySqlBackend',
        'HOST': '127.0.01',
        'PORT': 3306,
        'USER': 'root',
        'PASSWD': '123456',
        'DBNAME': 'testmysql',
    },
}