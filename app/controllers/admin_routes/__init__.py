from flask import render_template
from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.controllers.admin_routes import admin_tables
from app.controllers.admin_routes import manage_departments
from app.controllers.admin_routes import adminOverload
from app.controllers.admin_routes import termManagement
from app.controllers.admin_routes import adminManagement
from app.controllers.admin_routes import allPendingForms
from app.controllers.admin_routes import financialAidOverload
from app.controllers.admin_routes import emailTemplateController
