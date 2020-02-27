# Relying on https://www.oracle.com/technical-resources/articles/database/python-with-database-11g.html

import cx_Oracle
from app.config.loadConfig import*
from app import app

class banner():
    def __init__(self):
        secret_conf = get_secret_cfg()

        app.config["BANNER_PASSWORD"] = secret_conf['BANNER_PASSWORD']

        self.database_exists = False
        if env == 'production':
            self.database_exists = True
            try:
                self.conn = cx_Oracle.connect(
                        app.config["BANNER_USER"],
                        app.config["BANNER_PASSWORD"], 
                        app.config["BANNER_SERVER"])
                print(f"BANNER connection initialized. Oracle version {self.conn.version}")

            except Exception as err:
                print(f"BANNER connection failed: {err}")
                self.database_exists = False

    def canConnect:
        return bool(self.conn)

    def query(sql):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        return []

    def insert(data):
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        else:
            return True

