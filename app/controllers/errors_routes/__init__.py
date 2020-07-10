from flask import render_template
from flask import Blueprint
# from app.login_manager import require_login

error = Blueprint('errors_routes', __name__)
@error.context_processor
def inject_user():
    print('Inside of error routes?')
    currentUser = require_login()
    return {'currentUser': currentUser}

from app.controllers.errors_routes import handlers
