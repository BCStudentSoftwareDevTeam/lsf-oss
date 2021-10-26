from flask import render_template
from flask import Blueprint
# from app.login_manager import require_login
import os

local_login_bp = Blueprint('local_login', __name__)

from app.controllers.local_login_routes import local_login_routes
