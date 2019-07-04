from flask import Blueprint
from flask import render_template

bp = Blueprint('main', __name__)

from app.main_routes import main_routes
from app.main_routes import laborStatusForm

