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

###### This is the start of grabbing the data from the labor status form and displaying it on the Supervisor portal ######
    # Get all the forms from the supervisor form that has Scott as the Supervisor and order them by the endDate  #
    todayDate = date.today()
    print(todayDate)

    forms_by_supervisees = LaborStatusForm.select().where(LaborStatusForm.supervisor == current_user.username).order_by(LaborStatusForm.endDate.desc())
    # departmentID = Department.get(Department.DEPT_NAME == current_user.DEPT_NAME)
    # departmentStudents = LaborStatusForm.select().join(Term).where(LaborStatusForm.termCode.termEnd >= todayDate).where(LaborStatusForm.department == departmentID)

    # pastDepartmentStudents = LaborStatusForm.select().join(Term).where(LaborStatusForm.termCode.termEnd >= todayDate).where(LaborStatusForm.department == departmentID)
    currentDepartmentStudents = LaborStatusForm.select().join_from(LaborStatusForm, Term).join_from(LaborStatusForm, Department).where(LaborStatusForm.termCode.termEnd >= todayDate).where(LaborStatusForm.department.DEPT_NAME == current_user.DEPT_NAME)

    pastDepartmentStudents = LaborStatusForm.select().join_from(LaborStatusForm, Department).where(LaborStatusForm.department.DEPT_NAME == current_user.DEPT_NAME)

    # try:
    #  for i in departmentStudents:
    #      print(i)
    # except Exception as e:
    #     print(e)

    inactive_supervisees = []
    active_supervisees = []
    inactive = []
    active = []
    student_processed = False  # This variable dictates whether a student has already been added to the supervisor's portal
    end_date = None

    for supervisee in forms_by_supervisees: # go through all the form in the forms_by_supervisees
        try:
            tracy_supervisee = STUDATA.get(STUDATA.ID == supervisee.studentSupervisee.ID) # check if the student is in tracy to check if they're inactive or current
            for student in active_supervisees:
                if (supervisee.studentSupervisee.ID) == (student.studentSupervisee.ID):  # Checks whether student has already been added as an active student.
                    student_processed = True
            if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                active_supervisees.append(supervisee)
            else:
                student_processed = False  # Resets state machine.
        except: # if they are inactive
            for student in inactive_supervisees:
                if (supervisee.studentSupervisee.ID) == (student.studentSupervisee.ID):  # Checks whether student has already been added as an active student.
                    student_processed = True
            if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                inactive_supervisees.append(supervisee)
            else:
                student_processed = False  # Resets state machine


 ### Get the checkbox data from the HTML and send it to the download.py file through calling the excel.makeList function ###
    if request.method== 'POST':
        value =[]
        for form in active_supervisees:
            if request.form.get(form.studentSupervisee.ID):
                value.append( request.form.get(form.studentSupervisee.ID))

        for form in inactive_supervisees:
            if request.form.get(form.studentSupervisee.ID):
                value.append( request.form.get(form.studentSupervisee.ID))

        excel = ExcelMaker()
        completePath = excel.makeList(value)
        filename = completePath.split('/').pop()

    ## return the file path so the button will download the file ##
        return send_file(completePath,as_attachment=True, attachment_filename=filename)


    return render_template( 'main/index.html',
				    title=('Home'),
                    forms_by_supervisees = forms_by_supervisees,
                    active_supervisees = active_supervisees,
                    inactive_supervisees = inactive_supervisees,
                    username = current_user,
                    currentDepartmentStudents = currentDepartmentStudents,
                    pastDepartmentStudents = pastDepartmentStudents
                          )
