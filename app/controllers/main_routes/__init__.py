from flask import render_template
from flask import Blueprint
from app.config.loadConfig import *

main_bp = Blueprint('main', __name__)

from app.controllers.main_routes import main_routes
from app.controllers.main_routes import laborStatusForm
from app.controllers.admin_routes import adminManagement
from app.controllers.admin_routes import termManagement
from app.controllers.admin_routes import emailTemplateController
from app.controllers.main_routes import contributors
