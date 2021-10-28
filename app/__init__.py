from flask import Flask, session
from config2.config import config
import yaml
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
import os
from flask.helpers import get_env
from flask_login import LoginManager

# Initialize our application
app = Flask(__name__, template_folder="templates")

bootstrap = Bootstrap(app)

######### Set up Application Configuration #############
# Uses config2 - https://pypi.org/project/config2/ - with the addition of an uncommitted
# override yml to set instance parameters. By default, 'local-override.yaml'
#
# Precedence of configuration values is as follows:
#
# local-override.yaml
#     ↓
# environment file (e.g., development.yaml, production.yaml)
#     ↓
# default.yaml
#
##########################################################

# ensure ENV matches flask environment (for config2)
os.environ["ENV"] = get_env()

# Update application config from config2
app.config.update(config.get())

# Override configuration with our local instance configuration
from app.logic.utils import deep_update
with open("app/config/" + config.override_file, 'r') as ymlfile:
    try:
        deep_update(app.config, yaml.load(ymlfile, Loader=yaml.FullLoader))
    except TypeError:
        print(f"There was an error loading the override config file {config.override_file}. It might just be empty.")

# Set the secret key after configuration is set up
app.secret_key = app.config["secret_key"]


# Only use flask-login if Shibboleth is disabled
if app.config["USE_SHIBBOLETH"] == 0:
    login_mgr = LoginManager(app)  #FIXME: needs configured with our dev/prod environment handlers
    login_mgr.init_app(app)
    # Registers the admin interface blueprints
    from app.controllers.local_login_routes import local_login_bp as local_login_bp
    app.register_blueprint(local_login_bp)

# Registers blueprints (controllers). These are general routes, like /index
from app.controllers.main_routes import main_bp as main_bp
app.register_blueprint(main_bp)

# Registers the admin interface blueprints
from app.controllers.admin_routes import admin as admin_bp
app.register_blueprint(admin_bp)

# Registers error messaging
from app.controllers.errors_routes import error as errors_bp
app.register_blueprint(errors_bp)

# Makes the environment available globally
@app.context_processor
def inject_environment():
    return dict(env=get_env())

# Callback for loading the user.
# Function requires an input parameter, but we use session to grab username (instead of the parameter)
@login_mgr.user_loader
def load_user(user_id):
    from app.models.user import User
    if session.get("username", None):
        return User.get_or_none(username = session["username"])
