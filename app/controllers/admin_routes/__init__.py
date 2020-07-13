from flask import render_template
from flask import Blueprint
from app.login_manager import require_login

admin = Blueprint('admin', __name__)
@admin.context_processor
def injectUser():
    currentUser = require_login()
    return {'currentUser': currentUser}

from app.controllers.admin_routes import manage_departments
from app.controllers.admin_routes import termManagement
from app.controllers.admin_routes import adminManagement
from app.controllers.admin_routes import allPendingForms
from app.controllers.admin_routes import financialAidOverload
from app.controllers.admin_routes import emailTemplateController
