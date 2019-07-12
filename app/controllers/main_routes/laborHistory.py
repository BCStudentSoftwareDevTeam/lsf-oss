from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *

@main_bp.route('/laborhistory', methods=['GET', 'POST'])
# @login_required
def laborhistory():
    username = load_user('heggens')
    return render_template( 'main/laborhistory.html',
				            title=('Labor History'),
                            username = username
                          )
