# from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
# from flask_login import current_user, login_required
from flask import flash
from app.controllers.main_routes import *
from app.login_manager import *
from app.models.laborStatusForm import LaborStatusForm
from datetime import date


@main_bp.before_app_request
def before_request():
    pass # TODO Do we need to do anything here? User stuff?

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    current_user = require_login()
    #print(current_user)
    if not current_user:
        return render_template('errors/403.html')

    # Logged in
    # flash("Welcome to Labor Status forms. Delete this if flash messaging is working")
    forms_by_supervisees = LaborStatusForm.select(LaborStatusForm.studentSupervisee).where(LaborStatusForm.primarySupervisor == current_user.username).distinct()
    forms_by_POSN = LaborStatusForm.select(LaborStatusForm.POSN_TITLE).where(LaborStatusForm.primarySupervisor == current_user.username)
    for form in forms_by_supervisees:
        print(form)
    for Pos in forms_by_POSN:
        print(Pos)


    today = date.today()
    print("Today's date:", today)
    return render_template( 'main/index.html',
				    title=('Home'),
                    forms_by_supervisees = forms_by_supervisees,
                    username = current_user

                          )
