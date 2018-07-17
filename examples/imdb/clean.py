import pymysql
import examples.imdb.imdb.settings.backends as backends
import redis
import examples.imdb.imdb.settings.spider as spider_settings

mysql_settings = backends.BACKENDS['mysql']
host = mysql_settings.get('HOST')
port = mysql_settings.get('PORT')
username = mysql_settings.get('USER')
password = mysql_settings.get('PASSWD')
database = mysql_settings.get('DBNAME')
tablename = 'top250'
primary_key = 'movie'


redis_settings = backends.BACKENDS['redis']

SqlMoveItem = {
    'movie': 'VARCHAR(128)',
    'url': 'VARCHAR(255)',
    'rating': 'VARCHAR(255)',
    'spider': 'VARCHAR(255)',
}

if __name__ == '__main__':
    connection = pymysql.connect(
        user=username,
        password=password,
        host=host,
        port=port,
        charset='utf8'
    )

    connect_cursor = connection.cursor()

    command = 'drop database if exists %s' % database
    connect_cursor.execute(command)
    connect_cursor.execute("create database %s default character set utf8 collate utf8_general_ci" % database)
    connect_cursor.execute("use %s" % database)


    # create table
    cmd_create_format = 'create table %s(%s,PRIMARY KEY (%s))'
    cmd_create_body = []
    for (k,t) in SqlMoveItem.items():
        cmd_create_body.append('%s %s' % (k, t))
    cmd_create = cmd_create_format % (tablename, ','.join(cmd_create_body), primary_key)
    connect_cursor.execute(cmd_create)

    redis_pool = redis.ConnectionPool(host=redis_settings.get('HOST'), port=6379, decode_responses=True)
    redis_server = redis.StrictRedis(connection_pool=redis_pool)

    redis_server.delete(spider_settings.REQUESTER.get('CONTAINER_KEY'))
    redis_server.delete(spider_settings.REQUESTER.get('DEDUPLICATER_KEY'))

    reporter_prefix = spider_settings.REPORTER.get('REPORTER_PREFIX')
    keys = redis_server.keys(reporter_prefix+'*')
    for k in keys:
        redis_server.delete(k)



