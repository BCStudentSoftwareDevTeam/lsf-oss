from flask import render_template
from flask import Blueprint

main_bp = Blueprint('main', __name__)

from app.controllers.main_routes import main_routes
from app.controllers.main_routes import laborStatusForm
from app.controllers.main_routes import laborHistory
from app.controllers.main_routes import alterLSF
from app.controllers.main_routes import studentOverloadApp
from app.controllers.main_routes import contributors
from app.controllers.main_routes import download
from app.controllers.main_routes import laborReleaseForm
from app.controllers.main_routes import contributors
