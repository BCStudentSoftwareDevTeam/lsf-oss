from __future__ import print_function
'''
Include all imports in this file; it will be called at the beginning of all files.
'''
#Flask imports
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import g
from flask import url_for
from flask import flash
from flask import abort
from flask_admin import Admin
import time
import sys,os
import pprint

cfg = get_cfg()
secret_cfg = get_secret_cfg()
sys.dont_write_bytecode = True

''' Creates an Flask object; @app will be used for all decorators.
from: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
"A decorator is just a callable that takes a function as an argument and
returns a replacement function. See start.py for an example"
'''
app = Flask(__name__)
app.secret_key = secret_cfg['secret_key']
#from app import app
admin = Admin(app)
# Builds all the database connections on app run
# Don't panic, if you need clarification ask.
@app.before_request
def before_request():
    g.dbMain =  mainDB.get_conn()

@app.teardown_request
def teardown_request(exception):
    dbM = getattr(g, 'db', None)
    if (dbM is not None) and (not dbM.is_closed()):
      dbM.close()

@app.errorhandler(403)
def access_denied(e):
    return render_template('views/403.html', cfg=cfg), 403

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('views/404.html', cfg=cfg), 404

####FIXME:Fom models import??????? ####
