# from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
# from flask_login import current_user, login_required
from flask import flash
from app.controllers.main_routes import *
from app.login_manager import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.Tracy.studata import STUDATA
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
    #forms_by_supervisees = LaborStatusForm.select(LaborStatusForm.studentSupervisee).where(LaborStatusForm.primarySupervisor == current_user.username ).distinct()

    forms_by_supervisees = LaborStatusForm.select(LaborStatusForm.studentSupervisee).where(LaborStatusForm.primarySupervisor == current_user.username or LaborStatusForm.secondarySupervisor == current_user.username).order_by(LaborStatusForm.endDate).distinct()

    # print(forms_by_supervisees)
    # my_form = forms_by_supervisees
    # forms = my_form.select(LaborStatusForm.studentSupervisee).distinct()
    # for form in forms:
    #     print(form)
    #forms_by_supervisees = forms_by_supervisees.select(LaborStatusForm.studentSupervisee).distinct()
    # for form in forms_by_supervisees:
    #     print(form)
    inactive_supervisees = []
    active_supervisees = []
    inactive = []
    active = []
    for supervisee in forms_by_supervisees:
        try:
            tracy_supervisee = STUDATA.get(STUDATA.ID == supervisee.studentSupervisee.ID)
            #print(LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == supervisee.studentSupervisee))
            active = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == supervisee.studentSupervisee)[0]
            active_supervisees.append(active)
            # for form in active:
            #     print(form)
            #     active_supervisees.append(active)
        except:
            #print(LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == supervisee.studentSupervisee))
            inactive = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == supervisee.studentSupervisee)[0]

            inactive_supervisees.append(inactive)

        print(inactive_supervisees)


    today = date.today()
    print("Today's date:", today)
    return render_template( 'main/index.html',
				    title=('Home'),
                    forms_by_supervisees = forms_by_supervisees,
                    active_supervisees = active_supervisees,
                    inactive_supervisees = inactive_supervisees,
                    username = current_user

                          )
