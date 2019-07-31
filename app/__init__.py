from flask import Flask
import yaml
from flask_bootstrap import Bootstrap



app = Flask(__name__)
bootstrap = Bootstrap(app)
# login = LoginManager(app)  #FIXME: needs configured with our dev/prod environment handlers

def load_config(file):
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg

cfg = load_config("app/config/secret_config.yaml")
app.secret_key = cfg["secret_key"]

# Registers blueprints (controllers). These are general routes, like /index
from app.controllers.main_routes import main_bp as main_bp
app.register_blueprint(main_bp)

# Registers the admin interface blueprints
from app.controllers.admin_routes import admin as admin_bp
app.register_blueprint(admin_bp)

# Registers error messaging
from app.controllers.errors_routes import error as errors_bp
app.register_blueprint(errors_bp)
