from peewee import *

# from app import login
from app import load_config


def getMySQLDB():
    cfg = load_config('app/config/secret_config.yaml')
    theDB = MySQLDatabase(cfg['db']['db_name'], host = cfg['db']['host'], user = cfg['db']['username'], passwd = cfg['db']['password'])
    return theDB

mainDB = getMySQLDB() # MySQL (current)

class baseModel(Model):
    class Meta:
        database = mainDB
