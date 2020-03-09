# Relying on https://www.oracle.com/technical-resources/articles/database/python-with-database-11g.html

import cx_Oracle
from app.config.loadConfig import*
from app import app

class Banner():
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
        return self.database_exists

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

    def insert(data):
        if self.conn:
            try:
		# https://bitbucket.org/laborstudents/labor-status-forms/raw/bdcbaae27a2a13b8ff4351b1e63327c52151edf5/Admin/PendingLaborStatusForms.aspx.cs
		# All break positions should have 8 as the hours per day value. 
		# Hours (PZRLABRSTAT_HOUR) cannot be null in the Banner DB 

		# term_type is SUM, BRK or REG
                stmt = """
INSERT INTO pzrlabrstat (PZRLABRSTAT_FORM_ID, PZRLABRSTAT_SUPERVISEE, PZRLABRSTAT_SUPERVISOR, PZRLABRSTAT_JOBTYPE, PZRLABRSTAT_POSTION, PZRLABRSTAT_HOUR, PZRLABRSTAT_CONTRACT_HRS, PZRLABRSTAT_START_DATE, PZRLABRSTAT_CREATE_DATE, PZRLABRSTAT_ORG, PZRLABRSTAT_BREAK) 
VALUES ( :formID, :studentID, :superID, :jobType, :position, :hours, :long_break_hours, :start_date, :create_date, :org, :term_type )""".strip()
		params = {
                    ":formID": data[formID],
                    ":studentID": data[asdf],
                    ":superID": data[asdf],
                    ":jobType": data[asdf],
                    ":position": data[asdf],
                    ":hours": data[asdf],
                    ":long_break_hours": data[asdf],
                    ":start_date": data[asdf],
                    ":create_date": data[asdf],
                    ":org": data[asdf],
                    ":term_type": data[asdf]
                }

                cursor = self.conn.cursor()
                return cursor.execute(stmt, params)
            except Exception as err:
                print("Error inserting into BANNER db:", err)
                return False
        else:
            return None # The same as a succesful execution
