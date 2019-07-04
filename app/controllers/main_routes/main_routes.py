# from flask import render_template  #, flash, redirect, url_for, request, g, jsonify, current_app
# from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *

@main_bp.before_app_request
def before_request():
    pass #Do we need to do anything here? User stuff?

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    username = load_user('heggens')
    return render_template( 'main/index.html',
				            title=('Home'),
                            username = username
                          )
