from peewee import *
import os

# from app import login
from app import load_config


def getMySQLDB():
    cfg = load_config('app/config/secret_config.yaml')
    if os.environ.get("USING_CONTAINER", False):
        cfg['tracy']['host'] = 'db'
    else:
        cfg['tracy']['host'] = 'localhost'
    theDB = MySQLDatabase(cfg['tracy']['db_name'], host = cfg['tracy']['host'], user = cfg['tracy']['username'], passwd = cfg['tracy']['password'])
    return theDB

tracyDB = getMySQLDB() # MySQL (current)

class baseModel(Model):
    class Meta:
        database = tracyDB
