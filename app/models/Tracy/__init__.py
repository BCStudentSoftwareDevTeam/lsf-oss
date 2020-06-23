from flask_sqlalchemy import SQLAlchemy
from app import load_config, app

cfg = load_config('app/config/secret_config.yaml')
# production mssql+pyodbc_mssql
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}/{}".format(cfg['tracy']['username'], cfg['tracy']['password'], 'localhost', cfg['tracy']['db_name'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
