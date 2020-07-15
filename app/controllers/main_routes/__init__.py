from flask import render_template
from flask import Blueprint
from app.login_manager import require_login

main_bp = Blueprint('main', __name__)
@main_bp.context_processor
def injectUser():
    currentUser = require_login()
    return {'currentUser': currentUser}


from app.controllers.main_routes import main_routes
from app.controllers.main_routes import laborStatusForm
from app.controllers.main_routes import laborHistory
from app.controllers.main_routes import alterLSF
from app.controllers.main_routes import studentOverloadApp
from app.controllers.main_routes import contributors
from app.controllers.main_routes import download
from app.controllers.main_routes import laborReleaseForm
from app.controllers.main_routes import contributors
