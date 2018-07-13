import pymysql
import examples.spider_redis.spider_redis.settings.backends as backends

settings = backends.BACKENDS['mysql']
host = settings.get('HOST')
port = settings.get('PORT')
username = settings.get('USER')
password = settings.get('PASSWD')
database = settings.get('DBNAME')
tablename = 'testtable'

SqlMoveItem = {
    'name': 'VARCHAR(255)',
    'info': 'VARCHAR(255)',
    'rating': 'INT',
    'num': 'INT',
    'quote': 'VARCHAR(255)',
    'img_url': 'VARCHAR(255)',
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
    connect_cursor.execute("create database %s default character set utf8mb4 collate utf8mb4_unicode_ci" % database)
    connect_cursor.execute("use %s" % database)

    db_name = tablename
    db_primary_key = 'name'

    # create table
    cmd_create_format = 'create table %s(%s,PRIMARY KEY (%s))'
    cmd_create_body = []
    for (k,t) in SqlMoveItem.items():
        cmd_create_body.append('%s %s' % (k, t))
    cmd_create = cmd_create_format % (db_name, ','.join(cmd_create_body), db_primary_key)
    connect_cursor.execute(cmd_create)