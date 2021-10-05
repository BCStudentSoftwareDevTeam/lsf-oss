from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app#, load_config
import urllib3
from urllib.parse import quote
import os

# cfg = load_config('app/config/secret_config.yaml')

host = app.config['tracy']['host']
if not os.environ.get("USING_CONTAINER", False):
    host = "localhost"

# MySQL database connection
uri = "mysql+pymysql://{}:{}@{}/{}".format(app.config['tracy']['username'], app.config['tracy']['password'], host, app.config['tracy']['db_name'])

# MSSQL database connection
if app.config['USE_TRACY']:
    uri = "mssql+pyodbc:///?odbc_connect=" + quote('DRIVER=FreeTDS;SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_Version=8.0;'.format(app.config['tracy']['mssql_host'],  app.config['tracy']['db_name'], app.config['tracy']['mssql_user'], app.config['tracy']['mssql_password']))


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)
migrate = Migrate(app, db)
