# from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
# from flask_login import current_user, login_required
from flask import flash, send_file
from app.controllers.main_routes import *
from app.controllers.main_routes.download import ExcelMaker
from app.login_manager import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.Tracy.studata import STUDATA
from app.models.department import Department
from app.models.term import Term
from datetime import datetime, date


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

    # This is the start of grabbing the data from the labor status form and displaying it on the Supervisor portal
    # Get all the forms from the supervisor form that has Scott as the Supervisor and order them by the endDate  #
    todayDate = date.today()
    print(todayDate)
    # Grabs all the labor status forms where the current user is the supervisor
    formsBySupervisees = LaborStatusForm.select().where(LaborStatusForm.supervisor == current_user.username).order_by(LaborStatusForm.endDate.desc())
    # Grabs all the labor status forms where the current users department matches the status forms derpartment, and where the current date is less than the term end date on the status form
    currentDepartmentStudents = LaborStatusForm.select().join_from(LaborStatusForm, Term).join_from(LaborStatusForm, Department).where(LaborStatusForm.termCode.termEnd >= todayDate).where(LaborStatusForm.department.DEPT_NAME == current_user.DEPT_NAME)
    # Grabs all the labor status forms where the current users department matches the status forms derpartment
    allDepartmentStudents = LaborStatusForm.select().join_from(LaborStatusForm, Department).where(LaborStatusForm.department.DEPT_NAME == current_user.DEPT_NAME).order_by(LaborStatusForm.endDate.desc())


    inactiveSupervisees = []
    activeSupervisees = []
    inactive = []
    active = []
    student_processed = False  # This variable dictates whether a student has already been added to the supervisor's portal
    end_date = None

    for supervisee in formsBySupervisees: # go through all the form in the formsBySupervisees
        try:
            tracy_supervisee = STUDATA.get(STUDATA.ID == supervisee.studentSupervisee.ID) # check if the student is in tracy to check if they're inactive or current
            for student in activeSupervisees:
                if (supervisee.studentSupervisee.ID) == (student.studentSupervisee.ID):  # Checks whether student has already been added as an active student.
                    student_processed = True
            if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                activeSupervisees.append(supervisee)
            else:
                student_processed = False  # Resets state machine.
        except: # if they are inactive
            for student in inactiveSupervisees:
                if (supervisee.studentSupervisee.ID) == (student.studentSupervisee.ID):  # Checks whether student has already been added as an active student.
                    student_processed = True
            if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                inactiveSupervisees.append(supervisee)
            else:
                student_processed = False  # Resets state machine

    # On the click of the download button, 'POST' method will send all checked boxes from modal to excel maker
    if request.method== 'POST':
        value =[]
        for form in activeSupervisees:
            name = str(form.laborStatusFormID)
            if request.form.get(name):
                print("here")
                value.append( request.form.get(name))

        for form in inactiveSupervisees:
            name = str(form.laborStatusFormID)
            if request.form.get(name):
                value.append( request.form.get(name))

        for form in currentDepartmentStudents:
            name = str(form.laborStatusFormID)
            if request.form.get(name):
                value.append( request.form.get(name))

        for form in allDepartmentStudents:
            name = str(form.laborStatusFormID)
            if request.form.get(name):
                value.append( request.form.get(name))
        # Prevents 'POST' method from sending the same value twice to excel maker
        noDuplicateList = []
        for i in value:
            if i not in noDuplicateList:
                noDuplicateList.append(i)
            else:
                pass
        print(value)
        print(noDuplicateList)
        excel = ExcelMaker()
        completePath = excel.makeList(noDuplicateList)
        filename = completePath.split('/').pop()

        # Returns the file path so the button will download the file
        return send_file(completePath,as_attachment=True, attachment_filename=filename)


    return render_template( 'main/index.html',
				    title=('Home'),
                    activeSupervisees = activeSupervisees,
                    inactiveSupervisees = inactiveSupervisees,
                    username = current_user,
                    currentDepartmentStudents = currentDepartmentStudents,
                    allDepartmentStudents = allDepartmentStudents
                          )
