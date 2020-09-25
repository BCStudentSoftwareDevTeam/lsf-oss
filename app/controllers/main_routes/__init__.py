from flask import render_template
from flask import Blueprint
from flask import request
from app.login_manager import require_login
import os
import os.path
import urllib.parse

main_bp = Blueprint('main', __name__)
@main_bp.context_processor
def injectGlobalData():
    currentUser = require_login()
    lastStaticUpdate = str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk('app/static')
                   for f in files))
    dict = {
        "supervisorPortal":"2",
        "students":"3",
        "dept":"4",
        "lsf":"5",
        "admin":"6",
        "pending": "7",
        "overload": "8",
        "past": "9",
        "manageT": "10",
        "manageD": "11",
        "manageA": "12",
        "email": "13",
        "logout": "14"
    }

    return {'currentUser': currentUser,
            'lastStaticUpdate': lastStaticUpdate,
            'dictt': dict,
             #so that we can use request in the HTML
            }

from app.controllers.main_routes import main_routes
from app.controllers.main_routes import laborStatusForm
from app.controllers.main_routes import laborHistory
from app.controllers.main_routes import alterLSF
from app.controllers.main_routes import studentOverloadApp
from app.controllers.main_routes import contributors
from app.controllers.main_routes import download
from app.controllers.main_routes import laborReleaseForm
from app.controllers.main_routes import contributors
