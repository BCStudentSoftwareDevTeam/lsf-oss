# Relying on https://www.oracle.com/technical-resources/articles/database/python-with-database-11g.html

import cx_Oracle
from app.config.loadConfig import*
from app import app

class Banner():
    def __init__(self):
        secret_conf = get_secret_cfg()
        banner_cfg = secret_conf["banner"]

        self.database_exists = False
        if app.config['ENV'] == 'production':
            self.database_exists = True
            try:
                self.conn = cx_Oracle.connect( 
                        banner_cfg["user"], 
                        banner_cfg["password"], 
                        "{url}:{port}/{sid}".format(**banner_cfg))
                print("BANNER connection initialized. Oracle version {}".format(self.conn.version))

            except Exception as err:
                print("BANNER connection failed: {}: {}".format(type(err).__name__, err))
                self.database_exists = False
                raise err

    def canConnect(self):
        return self.database_exists

    def query(self, sql):
        if self.database_exists:
            try:
                cursor = self.conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as err:
                print("Error querying BANNER db:", err)
                return []
        return []

    def insert(self, data):
        """
        Add an official labor status form to BANNER. If no database connection exists, this method will act as 
        though the insert succeeds.
        
        Returns True if the insert succeeds, and False otherwise. A secondary return value also returns the execute() result.
        
        E.g., (result, cursor) = conn.insert(data)
        """

        if self.database_exists:
            # https://bitbucket.org/laborstudents/labor-status-forms/raw/bdcbaae27a2a13b8ff4351b1e63327c52151edf5/Admin/PendingLaborStatusForms.aspx.cs
            # All break positions should have 8 as the hours per day value. 
            # Hours (PZRLABRSTAT_HOUR) cannot be null in the Banner DB 

            # term_type is SUM, BRK or REG
            stmt = """INSERT INTO pzrlabrstat (PZRLABRSTAT_FORM_ID, PZRLABRSTAT_SUPERVISEE, PZRLABRSTAT_SUPERVISOR, PZRLABRSTAT_JOBTYPE, PZRLABRSTAT_POSTION, PZRLABRSTAT_HOUR, PZRLABRSTAT_CONTRACT_HRS, PZRLABRSTAT_START_DATE, PZRLABRSTAT_CREATE_DATE, PZRLABRSTAT_ORG, PZRLABRSTAT_BREAK) 
                VALUES ( :formID, :studentID, :superID, :jobType, :position, :hours, :long_break_hours, :start_date, :create_date, :org, :term_type )"""

            # data.FormID.termCode.termCode
            form = data.formID
            termCode = str(form.termCode.termCode)[-2:]
            termType = "REG"
            if termCode in ['01','02','03']:
                termType = "BRK"
            elif  termCode == '13':
                termType = "SUM"
                
            
            params = {
                ":formID": form.laborStatusFormID,
                ":studentID": form.studentSupervisee,
                ":superID": form.supervisor.username, # This could be shaky
                ":jobType": form.formID.jobType,
                ":position": data["position"],
                ":hours": data["hours"],
                ":long_break_hours": data["long_break_hours"],
                ":start_date": data["start_date"],
                ":create_date": data["create_date"],
                ":org": data["org"],
                ":term_type": termType
            }

            # Debugging
            print(data)
            print(params)
            return False, None
            # Debugging

            try:
                cursor = self.conn.cursor()
                result = cursor.execute(stmt, params)
                return (result == None), result

            except Exception as err:
                print("Error inserting into BANNER db:", err)
                return False, err
        else:
            return True, None # The same as a succesful execution
