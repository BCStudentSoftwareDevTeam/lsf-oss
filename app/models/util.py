from app.config.loadConfig import *
from app.logic.absolute_path import *
from peewee import *
import os

def getDB (dbName):
  config_abs_path = getAbsolutePath('app/config','config.yaml')
  cfg             = load_config(config_abs_path)
  db_abs_path     = getAbsolutePath(cfg['databases'][dbName])
  theDB           = SqliteDatabase (db_abs_path,
                          pragmas = ( ('busy_timeout',  100),
                                      ('journal_mode', 'WAL')
                                  ),
                          threadlocals = True)
  return theDB

def getMySQLDB():
  cfg           = load_config(getAbsolutePath("app/config", "config.yaml"))
#  print(cfg['db'])
  theDB         = MySQLDatabase(cfg['db']['db_name'], host = cfg['db']['host'], user = cfg['db']['username'], passwd = cfg['db']['password'])

  return theDB

mainDB = getMySQLDB() # MySQL (current)

class baseModel(Model):
  class Meta:
    database = mainDB

def checkStrings(strings):
  try:
    status = True
    for string in strings:
      if string == '':
        string = None
      if string != None:
        result = isinstance(str(string),str)
        if result == False:
          status = False
    return status
  except Exception as e:
    return False

def checkBooleans(booleans):
  status = True
  for bol in booleans:
    result = isinstance(bol,bool)
    if result == False:
      status = False
  return status

def checkIntegers(integers):
  status = True
  for num in integers:
    result = isinstance(num,int)
    if result == False:
      status = False
  return status
