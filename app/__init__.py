from flask import Flask
import yaml
from flask_bootstrap import Bootstrap
# from flask_login import LoginManager
# import cryptography

app = Flask(__name__)
bootstrap = Bootstrap(app)
# login = LoginManager(app)

def load_config(file):
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg

from app.main_routes import bp as main_bp
app.register_blueprint(main_bp)

from app.admin_routes import admin as admin_bp
app.register_blueprint(admin_bp)

from app.errors_routes import error as errors_bp
app.register_blueprint(errors_bp)

from app.models import *
