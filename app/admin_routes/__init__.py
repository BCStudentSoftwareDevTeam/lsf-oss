from flask import Blueprint
from flask import render_template

admin = Blueprint('admin', __name__)

from app.admin_routes import admin_tables
