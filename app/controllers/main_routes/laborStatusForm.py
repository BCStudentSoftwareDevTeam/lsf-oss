from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.status import *
from app.models.laborStatusForm import *
from app.models.overloadForm import *
from app.models.formHistory import *
from app.models.historyType import *
from app.models.term import *
from app.models.student import Student
from app.models.department import *
from flask import json, jsonify
from flask import request
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash
from app import cfg
from app.logic.emailHandler import*
from app.logic.userInsertFunctions import*
from app.models.supervisor import Supervisor
from app.logic.tracy import Tracy

@main_bp.route('/laborstatusform', methods=['GET'])
@main_bp.route('/laborstatusform/<laborStatusKey>', methods=['GET'])
def laborStatusForm(laborStatusKey = None):
    """ Render labor Status Form, and pre-populate LaborStatusForm page with the correct information when redirected from Labor History."""
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html'), 403
    if not currentUser.isLaborAdmin:
        if currentUser.student and not currentUser.supervisor:
            return redirect('/laborHistory/' + currentUser.student.ID)

    # Logged in
    students = Tracy().getStudents()
    terms = Term.select().where(Term.termState == "open") # changed to term state, open, closed, inactive
    staffs = Tracy().getSupervisors()
    departments = Tracy().getDepartments()

    # Only prepopulate form if current user is the supervisor or creator of the form.
    if laborStatusKey != None:
        selectedLSForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
        selectedFormHistory = FormHistory.get(FormHistory.formID == laborStatusKey)
        creator = selectedFormHistory.createdBy.supervisor.ID
        supervisor = selectedLSForm.supervisor.ID
        if currentUser.supervisor.ID == supervisor or currentUser.supervisor.ID == creator:
            forms = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey) # getting labor status form id, to prepopulate laborStatusForm.
        else:
            forms = None
    else:
        forms = None
    return render_template( 'main/laborStatusForm.html',
				            title=('Labor Status Form'),
                            UserID = currentUser,
                            forms = forms,
                            students = students,
                            terms = terms,
                            staffs = staffs,
                            departments = departments)

@main_bp.route('/laborstatusform/userInsert', methods=['POST'])
def userInsert():
    """ Create labor status form. Create labor history form. Most of the functions called here are in userInsertFunctions.py"""
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html'), 403
    rsp = (request.data).decode("utf-8")  # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    all_forms = []
    for i in range(len(rspFunctional)):
        tracyStudent = Tracy().getStudentFromBNumber(rspFunctional[i]['stuBNumber'])

        # Tries to get a student with the following information from the database
        # if the student doesn't exist, it tries to create a student with that same information
        try:
            createStudentFromTracyObj(tracyStudent)
        except InvalidUserException as e:
            print(e)
            return "", 500

        student = Student.get(ID = tracyStudent.ID)

        # Updates the student database with any updated attributes from TRACY
        student.FIRST_NAME = tracyStudent.FIRST_NAME            # FIRST_NAME
        student.LAST_NAME = tracyStudent.LAST_NAME              # LAST_NAME
        student.CLASS_LEVEL = tracyStudent.CLASS_LEVEL          # CLASS_LEVEL
        student.ACADEMIC_FOCUS = tracyStudent.ACADEMIC_FOCUS    # ACADEMIC_FOCUS
        student.MAJOR = tracyStudent.MAJOR                      # MAJOR
        student.PROBATION = tracyStudent.PROBATION              # PROBATION
        student.ADVISOR = tracyStudent.ADVISOR                  # ADVISOR
        student.STU_EMAIL = tracyStudent.STU_EMAIL              # STU_EMAIL
        student.STU_CPO = tracyStudent.STU_CPO                  # STU_CPO
        student.LAST_POSN = tracyStudent.LAST_POSN              # LAST_POSN
        student.LAST_SUP_PIDM = tracyStudent.LAST_SUP_PIDM      # LAST_SUP_PIDM

        student.save()                                          #Saves to student database

        studentID = student.ID
        d = createSupervisorFromTracy(bnumber=rspFunctional[i]['stuSupervisorID'])
        primarySupervisor = d.ID
        d, created = Department.get_or_create(DEPT_NAME = rspFunctional[i]['stuDepartment'])
        department = d.departmentID
        d, created = Term.get_or_create(termCode = rspFunctional[i]['stuTermCode'])
        term = d
        try:
            lsf = createLaborStatusForm(tracyStudent, studentID, primarySupervisor, department, term, rspFunctional[i])
            status = Status.get(Status.statusName == "Pending")
            creatorID = currentUser
            createOverloadFormAndFormHistory(rspFunctional[i], lsf, creatorID, status) # createOverloadFormAndFormHistory()
            try:
                emailDuringBreak(checkForSecondLSFBreak(term.termCode, studentID), term)
            except Exception as e:
                print("Error when sending emails during break: " + str(e))

            all_forms.append(True)
        except Exception as e:
            all_forms.append(False)
            print("ERROR on creating Labor Status Form/Overload Form" + str(e))

    flash("Form(s) submitted successfully! They will be eligible for approval in one business day.", "success")
    return jsonify(all_forms)

@main_bp.route("/laborstatusform/getDate/<termcode>", methods=['GET'])
def getDates(termcode):
    """ Get the start and end dates of the selected term. """
    dates = Term.select().where(Term.termCode == termcode)
    datesDict = {}
    for date in dates:
        start = date.termStart
        end  = date.termEnd
        primaryCutOff = date.primaryCutOff
        if primaryCutOff is None:
            datesDict[date.termCode] = {"Start Date":datetime.strftime(start, "%m/%d/%Y")  , "End Date": datetime.strftime(end, "%m/%d/%Y")}
        else:
            datesDict[date.termCode] = {"Start Date":datetime.strftime(start, "%m/%d/%Y")  , "End Date": datetime.strftime(end, "%m/%d/%Y"), "Primary Cut Off": datetime.strftime(primaryCutOff, "%m/%d/%Y"), "isBreak": date.isBreak, "isSummer": date.isSummer}
    return json.dumps(datesDict)

@main_bp.route("/laborstatusform/getPositions/<department>", methods=['GET'])
def getPositions(department):
    """ Get all of the positions that are in the selected department """
    positions = Tracy().getPositionsFromDepartment(department)
    positionDict = {}
    for position in positions:
        positionDict[position.POSN_CODE] = {"position": position.POSN_TITLE, "WLS":position.WLS}
    return json.dumps(positionDict)

@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>", methods=["POST"])
@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>/<isOneLSF>", methods=["GET"])
def checkForPrimaryOrSecondLSFBreak(termCode, student, isOneLSF=None):
    if isOneLSF:
        return checkForSecondLSFBreak(termCode, student)
    else:
        return checkForPrimaryPosition(termCode, student)

@main_bp.route("/laborstatusform/getcompliance/<department>", methods=["GET"])
def checkCompliance(department):
    """ Gets the compliance status of a department. """
    depts = Department.select().where(Department.ORG == department)
    deptDict = {}
    for dept in depts:
        deptDict['Department'] = {'Department Compliance': dept.departmentCompliance}
    return json.dumps(deptDict)

@main_bp.route("/laborstatusform/checktotalhours/<termCode>/<student>/<weeklyHours>/<contractHours>", methods=["GET"])
def checkTotalHours(termCode, student, weeklyHours, contractHours):
    """ Counts the total number of hours for the student after the new lsf is filled. """
    positions = FormHistory.select().join_from(FormHistory, LaborStatusForm).where(FormHistory.formID.termCode == termCode, FormHistory.formID.studentSupervisee == student, FormHistory.historyType == "Labor Status Form", (FormHistory.status == "Approved" or FormHistory.status == "Approved Reluctantly"))
    term = Term.get(Term.termCode == termCode)
    totalHours = 0
    for item in positions:
        formID = item.formID
        releasedForm = FormHistory.select().where(FormHistory.formID == formID, FormHistory.historyType == "Labor Release Form", FormHistory.status == "Approved")
        if not releasedForm:
            if term.isBreak:
                totalHours = totalHours + item.formID.contractHours
            else:
                totalHours = totalHours + item.formID.weeklyHours
    if term.isBreak:
        totalHours = totalHours + int(contractHours)
    else:
        totalHours = totalHours + int(weeklyHours)
    return json.dumps(totalHours)

@main_bp.route("/laborStatusForm/modal/releaseAndRehire", methods=['POST'])
def releaseAndRehire():
    try:
        currentUser = require_login()
        formID = eval(request.data.decode("utf-8"))
        laborStatusForm = LaborStatusForm.get(formID["formID"])

        todayDate = date.today()
        tomorrowDate = datetime.now()+timedelta(1)
        createLaborReleaseForm(currentUser, laborStatusForm, tomorrowDate, "Satisfactory", "None", "Approved", todayDate, currentUser)

        # Get student dict as data
        # using info in the dict find previous lsf
        # if lsf exists for primary: release the form
        # and create a new lsf using data in dict
        # otherwise, ... 

        return jsonify({"Success":True})
    except Exception as e:
        print("error", e)
        return jsonify({"Success": False})
