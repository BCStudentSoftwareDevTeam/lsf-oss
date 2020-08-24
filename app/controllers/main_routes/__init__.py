from flask import render_template
from flask import Blueprint
from app.login_manager import require_login
import os

main_bp = Blueprint('main', __name__)
@main_bp.context_processor
def injectGlobalData():
    currentUser = require_login()
    lastStaticUpdate = str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk('app/static')
                   for f in files))
    dict = {
        "students":"2",
        "dept":"3",
        "lsf":"4",
        "admin":"5",
        "pending": "6",
        "overload": "7",
        "past": "8",
        "manageT": "9",
        "manageD": "10",
        "manageA": "11",
        "email": "12",
        "logout": "13"

    }
    return {'currentUser': currentUser,
            'lastStaticUpdate': lastStaticUpdate,
            'dict': dict}

from app.controllers.main_routes import main_routes
from app.controllers.main_routes import laborStatusForm
from app.controllers.main_routes import laborHistory
from app.controllers.main_routes import alterLSF
from app.controllers.main_routes import studentOverloadApp
from app.controllers.main_routes import contributors
from app.controllers.main_routes import download
from app.controllers.main_routes import laborReleaseForm
from app.controllers.main_routes import contributors
