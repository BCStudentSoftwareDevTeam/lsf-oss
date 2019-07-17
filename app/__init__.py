from flask import Flask
import yaml
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *


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

# Configures the navigation bar
nav = Nav()


@nav.navigation()
def thenavbar():
    return Navbar(
        'Labor Status Forms',
        Subgroup(
            'Supervisor Portal',
            View('Current Labor Students',"main.index"),# 'main.currentLaborStudents'),   #FIXME this link will not work because it does not exist yet
            View('Labor Release Form', "main.index"), #'main.laborReleaseForm'),
            View('Past Labor Students', "main.index"),# 'main.pastLaborStudents'),         #FIXME this link will not work because it does not exist yet
            View('All Labor Students', "main.index"),#'main.allLaborStudents')            #FIXME this link will not work because it does not exist yet
            ),
        Subgroup(
            'Administration',
            View('Pending Forms', "main.index"),#'main.pendingForms'),                    #FIXME this link will not work because it does not exist yet
            View('Overload Forms', 'main.index'),
            View('All past forms', "main.index"),#'main.allPastForms'),                   #FIXME this link will not work because it does not exist yet
            View('Manage Terms', "main.index"), #'admin.term_Management'),
            View('Manage Departments', 'main.index'),  #FIXME this link will not work because it does not exist yet
            View('Manage Admins', "admin.admin_tables"), #'admin.admin_management'),
            View('Manage Email Templates', "main.index")# 'admin.email_templates')
            ),
        View('Labor Status Form', 'main.laborStatusForm'),
        View('Logout', 'main.index')
            )

nav.register_element('side', nav)

nav.init_app(app)
