from spiderman.contrib.backends.backend import BaseBackend
import pymysql


class MySqlBackend(BaseBackend):
    connection = None
    connect_cursor = None

    def __init__(self, settings):
        self.host = settings.get('HOST')
        self.port = settings.get('PORT')
        self.username = settings.get('USER')
        self.password = settings.get('PASSWD')
        self.database = settings.get('DBNAME')

    def start(self):
        if self.is_running():
            return

        super(MySqlBackend,self).start()

        self.connection = pymysql.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            charset='utf8'
        )
        self.connect_cursor = self.connection.cursor()
        self.connect_cursor.execute("use %s" % self.database)

    def stop(self, reason):
        if self.is_valid():
            self.connect_cursor.close()
            self.connection.commit()
            self.connection.close()

        self.connect_cursor = None
        self.connection = None

    def is_valid(self):
        if self.connection is None:
            return False
        if self.connect_cursor is None:
            return False
        return True

    def insert(self, tablename, item):
        if not self.is_valid():
            return

        # insert item
        cmd_format = "insert into %s(%s) value(%s)"
        cmd_title = []
        cmd_value = []

        for (k,v) in item.items():
            cmd_title.append(str(k))
            if isinstance(v, str):
                cmd_value.append("'{0}'".format(pymysql.escape_string(v)))
            else:
                cmd_value.append(pymysql.escape_string(v))

        cmd_insert = cmd_format % (tablename, ','.join(cmd_title), ','.join(cmd_value))
        self.execute_command(cmd_insert)

    def delete(self):
        pass

    def update(self):
        pass

    def query(self):
        pass

    def execute_command(self, cmd):
        if not self.is_valid():
            return
        self.connect_cursor.execute(cmd)
        self.connection.commit()
