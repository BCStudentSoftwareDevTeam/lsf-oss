# from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
# from flask_login import current_user, login_required
from flask import flash
from app.controllers.main_routes import *
from app.models.user import *
from app.login_manager import *

@main_bp.before_app_request
def before_request():
    pass #Do we need to do anything here? User stuff?

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    username = require_login()
    # flash("Welcome to Labor Status forms. Delete this if flash messaging is working")
    return render_template( 'main/index.html',
				            title=('Home'),
                            username = username
                          )
