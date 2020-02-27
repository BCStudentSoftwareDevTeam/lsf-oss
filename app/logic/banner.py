# Relying on https://www.oracle.com/technical-resources/articles/database/python-with-database-11g.html

import cx_Oracle
from app.config.loadConfig import*
from app import app

class banner():
    def __init__(self):
        secret_conf = get_secret_cfg()

        app.config["banner"]["password"] = secret_conf['BANNER_PASSWORD']
        banner_cfg = app.config["banner"]

        self.database_exists = False
        if env == 'production':
            self.database_exists = True
            try:
                self.conn = cx_Oracle.connect( 
                        banner_cfg["user"], 
                        banner_cfg["password"], 
                        "{url}:{port}/{sid}".format(**banner_cfg))
                print("BANNER connection initialized. Oracle version {}".format(self.conn.version))

            except Exception as err:
                print("BANNER connection failed: {}".format(err))
                self.database_exists = False

    def canConnect:
        return bool(self.conn)

    def query(sql):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as err:
                print("Error querying BANNER db:", err)
                return []
        return []

    def insert(sql):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                return cursor.execute(sql)
            except Exception as err:
                print("Error inserting into BANNER db:", err)
                return False
        else:
            return None # The same as a succesful execution
