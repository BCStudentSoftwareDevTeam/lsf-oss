from flask import Flask
import yaml
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
# from flask_login import LoginManager

app = Flask(__name__)
bootstrap = Bootstrap(app)
# login = LoginManager(app)  #FIXME: needs configured with our dev/prod environment handlers

def load_config(file):
    with open(file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


# Registers blueprints (controllers). These are general routes, like /index
from app.controllers.main_routes import main_bp as main_bp
app.register_blueprint(main_bp)

# Registers the admin interface blueprints
from app.controllers.admin_routes import admin as admin_bp
app.register_blueprint(admin_bp)

# Registers error messaging
from app.controllers.errors_routes import error as errors_bp
app.register_blueprint(errors_bp)

# Configures the navigation bar
nav = Nav()


@nav.navigation()
def thenavbar():
    return Navbar(
        'Labor Status Forms',
        View('Home', 'main.index'),
        View('Labor Status Form', 'main.laborStatusForm'),
        View("Administration", "admin.admin_tables")
    )

nav.init_app(app)
