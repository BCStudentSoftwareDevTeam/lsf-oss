# from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
# from flask_login import current_user, login_required
from flask import flash
from app.controllers.main_routes import *
<<<<<<< HEAD
from app.models.user import *
from app.models.laborStatusForm import LaborStatusForm
=======
from app.login_manager import *
>>>>>>> 7e5f7dab2e9f37fa1d2ffde8257b2d1991801312

@main_bp.before_app_request
def before_request():
    pass # TODO Do we need to do anything here? User stuff?

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    current_user = require_login()
    if not current_user:
        return render_template('errors/403.html')

    # Logged in
    # flash("Welcome to Labor Status forms. Delete this if flash messaging is working")
    forms_by_supervisees = LaborStatusForm.select(LaborStatusForm.studentSupervisee).where(LaborStatusForm.primarySupervisor == username.username).distinct()
    # for form in forms:
    #     print(form.studentSupervisee.FIRST_NAME)
    return render_template( 'main/index.html',
				            title=('Home'),
<<<<<<< HEAD
                            username = username,
                            forms_by_supervisees = forms_by_supervisees
=======
                            username = current_user
>>>>>>> 7e5f7dab2e9f37fa1d2ffde8257b2d1991801312
                          )
