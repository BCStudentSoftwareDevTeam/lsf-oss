from flask import render_template
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.controllers.main_routes import main_routes
from app.controllers.main_routes import laborStatusForm
from app.controllers.main_routes import laborReleaseForm
