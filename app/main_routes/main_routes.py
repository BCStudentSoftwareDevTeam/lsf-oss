from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app.main_routes import bp
from app.models.user import *

@bp.before_app_request
def before_request():
    pass #Do we need to do anything here? User stuff?

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    username = load_user('heggens')
    return render_template( 'index.html',
				            title=('Home'),
                            username = username
                          )
