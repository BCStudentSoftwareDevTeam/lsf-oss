from flask import render_template
from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.controllers.admin_routes import admin_tables
