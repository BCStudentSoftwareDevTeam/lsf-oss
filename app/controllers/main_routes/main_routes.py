from flask import flash, send_file
from app.controllers.main_routes import *
from app.controllers.main_routes.download import ExcelMaker
from app.login_manager import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.department import Department
from app.models.term import Term
from app.models.historyType import HistoryType
from app.models.formHistory import FormHistory
from datetime import datetime, date
from flask import request, redirect
from flask import json, jsonify
from flask import make_response
from app.logic.tracy import Tracy
from app.logic.tracy import InvalidQueryException
import app.login_manager as login_manager
import base64


@main_bp.before_app_request
def before_request():
    pass # TODO Do we need to do anything here? User stuff?

@main_bp.route('/logout', methods=['GET'])
def logout():
    return redirect(login_manager.logout())

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    try:
        currentUser = require_login()
        if not currentUser:
            return render_template('errors/403.html'), 403
        if not currentUser.isLaborAdmin:
            if currentUser.student and not currentUser.supervisor:   # logged in as a student
                return redirect('/laborHistory/' + currentUser.student.ID)
            if currentUser.supervisor:       # logged in as a Supervisor
                # Checks all the forms where the current user has been the creator or the supervisor, and grabs all the departments associated with those forms. Will only grab each department once.
                departments = FormHistory.select(FormHistory.formID.department.DEPT_NAME) \
                                .join_from(FormHistory, LaborStatusForm) \
                                .join_from(LaborStatusForm, Department) \
                                .where((FormHistory.formID.supervisor == currentUser.supervisor.ID) | (FormHistory.createdBy == currentUser)) \
                                .order_by(FormHistory.formID.department.DEPT_NAME.asc()) \
                                .distinct()
        else:   # logged in as an admin
            # Grabs every single department that currently has at least one labor status form in it
            departments = FormHistory.select(FormHistory.formID.department.DEPT_NAME) \
                            .join_from(FormHistory, LaborStatusForm) \
                            .join_from(LaborStatusForm, Department) \
                            .order_by(FormHistory.formID.department.DEPT_NAME.asc()) \
                            .distinct()

        todayDate = date.today()
        # Grabs all the labor status forms where the current user is the supervisor
        formsBySupervisees = []
        if currentUser.supervisor:
            formsBySupervisees = FormHistory.select().join_from(FormHistory, LaborStatusForm).join_from(FormHistory, HistoryType).where(FormHistory.formID.supervisor == currentUser.supervisor.ID,
            FormHistory.historyType.historyTypeName == "Labor Status Form").order_by(FormHistory.formID.endDate.desc())

        inactiveSupervisees = []
        currentSupervisees = []
        pastSupervisees = []
        student_processed = False  # This variable dictates whether a student has already been added to the supervisor's portal

        for supervisee in formsBySupervisees: # go through all the form in the formsBySupervisees
            try:
                tracy_supervisee = Tracy().getStudentFromBNumber(supervisee.formID.studentSupervisee.ID) # check if the student is in tracy to check if they're inactive or current

            except InvalidQueryException: # if they are inactive
                for student in inactiveSupervisees:
                    if (supervisee.formID.studentSupervisee.ID) == (student.formID.studentSupervisee.ID):  # Checks whether student has already been added as an active student.
                        student_processed = True
                if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                    inactiveSupervisees.append(supervisee)
            else: # if there is no exception (student is in Tracy and active) this code will run
                for student in currentSupervisees:
                    if (supervisee.formID.studentSupervisee.ID) == (student.formID.studentSupervisee.ID):  # Checks whether student has already been added as an current student.
                        student_processed = True
                for student in pastSupervisees:
                    if (supervisee.formID.studentSupervisee.ID) == (student.formID.studentSupervisee.ID):  # Checks whether student has already been added as an past student.
                        student_processed = True
                if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                    if supervisee.formID.endDate < todayDate:
                        pastSupervisees.append(supervisee)
                    elif supervisee.formID.endDate >= todayDate:
                        studentFormHistory = FormHistory.select().where(FormHistory.formID == supervisee.formID.laborStatusFormID).order_by(FormHistory.formHistoryID.desc())[0]
                        if studentFormHistory.historyType.historyTypeName == "Labor Release Form":
                            if studentFormHistory.status.statusName == "Approved":
                                pastSupervisees.append(supervisee)
                            else:
                                currentSupervisees.append(supervisee)
                        else:
                            currentSupervisees.append(supervisee)
            finally:# it will run at the end regardless of whether or no the excpet statement or else statement is met.
                student_processed = False  # Resets state machine.

        # On the click of the download button, 'POST' method will send all checked boxes from modal to excel maker
        if request.method== 'POST':
            value =[]
            # The "Try" and "Except" block here is needed because if the user tries to use the download button before they chose
            # a department from the Department dropdown, it will throw a NameError. The reason behind the error is because the vairbales
            # "currentDepartmentStudents", "allDepartmentStudents", and "inactiveDepStudent" are empty until the user chooses a department, so
            # trying to iterate through the empty variables causes the error. The "Try" and "Except" blocks will catch this error so that
            # a user can use the download button before they chose a department.
            try:
                for form in currentDepartmentStudents:
                    name = str(form.formID.laborStatusFormID)
                    if request.form.get(name):
                        value.append(request.form.get(name))
                for form in allDepartmentStudents:
                    name = str(form.formID.laborStatusFormID)
                    if request.form.get(name):
                        value.append(request.form.get(name))
                for form in inactiveDepStudent:
                    name = str(form.formID.laborStatusFormID)
                    if request.form.get(name):
                        value.append(request.form.get(name))
            except NameError as e:
                print("The runtime error happens because a department has not yet been selected.")
            for form in currentSupervisees:
                name = str(form.formID.laborStatusFormID)
                if request.form.get(name):
                    value.append( request.form.get(name))
            for form in pastSupervisees:
                name = str(form.formID.laborStatusFormID)
                if request.form.get(name):
                    value.append( request.form.get(name))
            for form in inactiveSupervisees:
                name = str(form.formID.laborStatusFormID)
                if request.form.get(name):
                    value.append( request.form.get(name))


            # Prevents 'POST' method from sending the same value twice to excel maker
            noDuplicateList = []
            for i in value:
                if i not in noDuplicateList:
                    noDuplicateList.append(i)
                else:
                    pass
            excel = ExcelMaker()
            completePath = excel.makeList(noDuplicateList)
            filename = completePath.split('/').pop()

            # Returns the file path so the button will download the file
            return send_file(completePath,as_attachment=True, attachment_filename=filename)
        return render_template( 'main/index.html',
    				    title=('Home'),
                        currentSupervisees = currentSupervisees,
                        pastSupervisees = pastSupervisees,
                        inactiveSupervisees = inactiveSupervisees,
                        UserID = currentUser,
                        currentUserDepartments = departments
                              )
    except Exception as e:
        #TODO We have to return some sort of error page
        print('Error in Supervisor Portal:', e)
        return "",500

@main_bp.route('/main/department/<departmentSelected>', methods=['GET'])
def populateDepartment(departmentSelected):
    try:
        currentUser = require_login()
        todayDate = date.today()

        if departmentSelected == "all":
            if currentUser.isLaborAdmin:
                formsByDept = FormHistory.select().join_from(FormHistory, LaborStatusForm)\
                                         .join_from(FormHistory, HistoryType)\
                                         .where(FormHistory.historyType.historyTypeName == "Labor Status Form")\
                                         .order_by(FormHistory.formID.endDate.desc())
            elif currentUser.supervisor:
                formsByDept = FormHistory.select().join_from(FormHistory, LaborStatusForm)\
                                         .join_from(FormHistory, HistoryType)\
                                         .where((FormHistory.formID.supervisor == currentUser.supervisor.ID) | (FormHistory.createdBy == currentUser))\
                                         .where(FormHistory.historyType.historyTypeName == "Labor Status Form")\
                                         .order_by(FormHistory.formID.endDate.desc())
        else:
            department = Department.get(Department.DEPT_NAME == departmentSelected)
            departmentPositions = Tracy().getPositionsFromDepartment(department.ORG, department.ACCOUNT)
            validPositions = []
            for position in departmentPositions:
                validPositions.append(position.POSN_CODE)
        # This will retrieve all the forms that are tied to the department the user selected from the select picker
            formsByDept = FormHistory.select().join_from(FormHistory, LaborStatusForm).join_from(FormHistory, HistoryType).where((FormHistory.historyType.historyTypeName == "Labor Status Form") & (FormHistory.formID.POSN_CODE << validPositions)).order_by(FormHistory.formID.endDate.desc())
        # These three variables need to be global variables because they need to be iterated through in the "POST" call
        global currentDepartmentStudents
        global allDepartmentStudents
        global inactiveDepStudent

        currentDepartmentStudents = []
        allDepartmentStudents = []
        inactiveDepStudent = []
        student_processed = False  # This variable dictates whether a student has already been added to the supervisor's portal

        for supervisee in formsByDept: # go through all the form in the formsBySupervisees
            try:
                tracy_supervisee = Tracy().getStudentFromBNumber(supervisee.formID.studentSupervisee.ID) # check if the student is in tracy to check if they're inactive or current

            except InvalidQueryException: # if they are inactive
                for student in inactiveDepStudent:
                    if (supervisee.formID.studentSupervisee.ID) == (student.formID.studentSupervisee.ID):  # Checks whether student has already been added as an active student.
                        student_processed = True
                if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                    inactiveDepStudent.append(supervisee)
            else: # if there is no exception (student is in Tracy and active) this code will run
                for student in currentDepartmentStudents:
                    if (supervisee.formID.studentSupervisee.ID) == (student.formID.studentSupervisee.ID):  # Checks whether student has already been added as an current student.
                        student_processed = True
                for student in allDepartmentStudents:
                    if (supervisee.formID.studentSupervisee.ID) == (student.formID.studentSupervisee.ID):  # Checks whether student has already been added as an past student.
                        student_processed = True
                if student_processed == False:  # If a student has not yet been added to the view, they are appended as an active student.
                    # If a forms "endDate" is less than today's date, then we know the form is from the past and will go into "All Departments"
                    if supervisee.formID.endDate < todayDate:
                        allDepartmentStudents.append(supervisee)
                    # If a forms "endDate" is greater than today's date, then we need to look at other conditions
                    elif supervisee.formID.endDate >= todayDate:
                        # For every form at this point, we need to see if there are any "Labor Release Forms" tied to the form
                        studentFormHistory = FormHistory.select().where(FormHistory.formID == supervisee.formID.laborStatusFormID).order_by(FormHistory.formHistoryID.desc())[0]
                        if studentFormHistory.historyType.historyTypeName == "Labor Release Form":
                            # If the form has a "Labor Release Form" with a status of "Approved", then we know the student is no longer employed
                            if studentFormHistory.status.statusName == "Approved":
                                allDepartmentStudents.append(supervisee)
                            # If the form has a "Labor Release Form" with a status not equal to "Approved", then we know the student is still employed
                            else:
                                currentDepartmentStudents.append(supervisee)
                        # If the form does not have a "Labor Release Form", then we know the student is still employed
                        else:
                            currentDepartmentStudents.append(supervisee)
            finally: # it will run at the end regardless of whether or no the excpet statement or else statement is met.
                student_processed = False  # Resets state machine.



        # This section will format our JSON data with the key-value pairs we want to pass back to the AJAX call in our JS file.
        departmentStudents = []
        for i in currentDepartmentStudents:
            departmentStudents.append({"Status":"Current Department Students",
                                        "Student": i.formID.studentSupervisee.FIRST_NAME + " " + i.formID.studentSupervisee.LAST_NAME,
                                        "BNumber": i.formID.studentSupervisee.ID,
                                        "Term": i.formID.termCode.termName,
                                        "Position": i.formID.POSN_TITLE,
                                        "checkboxModalClass" : "currentDepartmentModal",
                                        "activeStatus" : "True",
                                        "formID" : i.formID.laborStatusFormID,
                                        "Department": i.formID.department.DEPT_NAME,
                                        "formStatus": i.status.statusName})
        for i in allDepartmentStudents:
            departmentStudents.append({"Status":"All Department Students",
                                        "Student": i.formID.studentSupervisee.FIRST_NAME + " " + i.formID.studentSupervisee.LAST_NAME,
                                        "BNumber": i.formID.studentSupervisee.ID,
                                        "Term": i.formID.termCode.termName,
                                        "Position": i.formID.POSN_TITLE,
                                        "checkboxModalClass" : "allDepartmentModal",
                                        "activeStatus" : "True",
                                        "formID" : i.formID.laborStatusFormID,
                                        "Department": i.formID.department.DEPT_NAME,
                                        "formStatus": "Past Student"})
        for i in inactiveDepStudent:
            departmentStudents.append({"Status":"All Department Students",
                                    "Student": i.formID.studentSupervisee.FIRST_NAME + " " + i.formID.studentSupervisee.LAST_NAME,
                                    "BNumber": i.formID.studentSupervisee.ID,
                                    "Term": i.formID.termCode.termName,
                                    "Position": i.formID.POSN_TITLE,
                                    "checkboxModalClass" : "allDepartmentModal",
                                    "activeStatus" : "False",
                                    "formID" : i.formID.laborStatusFormID,
                                    "Department": i.formID.department.DEPT_NAME,
                                    "formStatus": i.status.statusName})
        return json.dumps(departmentStudents)

    except Exception as e:
        print('ERROR in Department Stundents:', e)
        return jsonify({"Success": False})
