import pymysql
import examples.imdb.imdb.settings.backends as backends

settings = backends.BACKENDS['mysql']
host = settings.get('HOST')
port = settings.get('PORT')
username = settings.get('USER')
password = settings.get('PASSWD')
database = settings.get('DBNAME')
tablename = 'testtable'
primary_key = 'rating'

SqlMoveItem = {
    'movie': 'VARCHAR(255)',
    'url': 'VARCHAR(255)',
    'rating': 'INT',
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
    connect_cursor.execute("create database %s default character set utf8mb4 collate utf8mb4_unicode_ci" % database)
    connect_cursor.execute("use %s" % database)


    # create table
    cmd_create_format = 'create table %s(%s,PRIMARY KEY (%s))'
    cmd_create_body = []
    for (k,t) in SqlMoveItem.items():
        cmd_create_body.append('%s %s' % (k, t))
    cmd_create = cmd_create_format % (tablename, ','.join(cmd_create_body), primary_key)
    connect_cursor.execute(cmd_create)