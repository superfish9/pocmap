#coding=utf-8

import sqlite3

class Database(object):
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
            except sqlite3.OperationalError, ex:
                if not "locked" in getSafeExString(ex):
                    raise
            else:
                break

        if statement.lstrip().upper().startswith("SELECT"):
            return self.cursor.fetchall()
            
    def init(self):
        self.execute("CREATE TABLE logs("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                  "taskid INTEGER, time TEXT, "
                  "level TEXT, message TEXT"
                  ")")

        self.execute("CREATE TABLE data("
                  "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                  "taskid INTEGER, status INTEGER, "
                  "content_type INTEGER, value TEXT"
                  ")")

        self.execute("CREATE TABLE errors("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "taskid INTEGER, error TEXT"
                    ")")
