#coding=utf-8

import sqlite3

class Database(object):
    '''
    database handle for sqlite3.
    '''
    filepath = 'data/pocmapapi.db'

    def __init__(self, database=None):
        self.database = self.filepath if database is None else database
        self.connection = None
        self.cursor = None

    def connect(self, who="server"):
        self.connection = sqlite3.connect(self.database, timeout=3, isolation_level=None)
        self.cursor = self.connection.cursor()
        
    def disconnect(self):
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def execute(self, statement, arguments=None):
        while True:
            try:
                if arguments:
                    self.cursor.execute(statement, arguments)
                else:
                    self.cursor.execute(statement)
                self.commit()
            except sqlite3.OperationalError, ex:
                    raise
            else:
                break

        if statement.lstrip().upper().startswith("SELECT"):
            return self.cursor.fetchall()
            
    def init(self):
        self.execute("CREATE TABLE data("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                  "taskid CHAR(16), status CHAR(16), "
                  "vuls CHAR(1024)"
                  ")")
