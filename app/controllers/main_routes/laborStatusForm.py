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
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.department import *
from app.models.Tracy.stuposn import STUPOSN
from flask import json, jsonify
from flask import request
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash
from app import cfg
from app.logic.emailHandler import*
from app.logic.userInsertFunctions import*

@main_bp.route('/laborstatusform', methods=['GET'])
@main_bp.route('/laborstatusform/<laborStatusKey>', methods=['GET'])
def laborStatusForm(laborStatusKey = None):
    """ Render labor Status Form, and pre-populate LaborStatusForm page with the correct information when redirected from Labor History."""
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html')
    if not currentUser.isLaborAdmin:       # Not an admin
        isLaborAdmin = False
    else:
        isLaborAdmin = True
    # Logged in
    wls = STUPOSN.select(STUPOSN.WLS).distinct() # getting WLS from TRACY
    posnCode = STUPOSN.select(STUPOSN.POSN_CODE).distinct() # getting position code from TRACY
    students = STUDATA.select().order_by(STUDATA.FIRST_NAME.asc()) # getting student names from TRACY
    terms = Term.select().where(Term.termState == "open") # changed to term state, open, closed, inactive
    staffs = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # getting supervisors from TRACY
    departments = STUPOSN.select(STUPOSN.ORG, STUPOSN.DEPT_NAME, STUPOSN.ACCOUNT).distinct() # getting department names from TRACY

    # Only prepopulate form if current user is the supervisor or creator of the form.
    if laborStatusKey != None:
        selectedLSForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
        selectedFormHistory = FormHistory.get(FormHistory.formID == laborStatusKey)
        creator = selectedFormHistory.createdBy.username
        supervisor = selectedLSForm.supervisor.username
        if currentUser.username == supervisor or currentUser.username == creator:
            forms = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey) # getting labor status form id, to prepopulate laborStatusForm.
        else:
            forms = None
            return render_template('errors/403.html')
    else:
        forms = None
    return render_template( 'main/laborStatusForm.html',
				            title=('Labor Status Form'),
                            UserID = currentUser,
                            forms = forms,
                            students = students,
                            terms = terms,
                            staffs = staffs,
                            departments = departments,
                            isLaborAdmin = isLaborAdmin)

@main_bp.route('/laborstatusform/userInsert', methods=['POST'])
def userInsert():
    """ Create labor status form. Create labor history form. Most of the functions called here are in userInsertFunctions.py"""
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html')
    rsp = (request.data).decode("utf-8")  # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    all_forms = []
    for i in range(len(rspFunctional)):
        tracyStudent = STUDATA.get(ID = rspFunctional[i]['stuBNumber']) #Gets student info from Tracy
        #Tries to get a student with the followin information from the database
        #if the student doesn't exist, it tries to create a student with that same information
        try:
            getOrCreateStudentData(tracyStudent)
        except Exception as e:
            print("ERROR: ", e)

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
        d, created = User.get_or_create(UserID = rspFunctional[i]['stuSupervisorID'])
        primarySupervisor = d.UserID
        d, created = Department.get_or_create(DEPT_NAME = rspFunctional[i]['stuDepartment'])
        department = d.departmentID
        d, created = Term.get_or_create(termCode = rspFunctional[i]['stuTermCode'])
        term = d
        try:
            lsf = createLaborStatusForm(tracyStudent, studentID, primarySupervisor, department, term, rspFunctional[i])
            status = Status.get(Status.statusName == "Pending")
            d, created = User.get_or_create(username = currentUser.username)
            creatorID = d.UserID
            createOverloadFormAndFormHistory(rspFunctional[i], lsf, creatorID, status) # createOverloadFormAndFormHistory()
            try:
                emailDuringBreak(checkForSecondLSFBreak(term.termCode, studentID, "lsf"), term)
            except Exception as e:
                print("Error on sending emails during break: " + str(e))

            all_forms.append(True)
        except Exception as e:
            all_forms.append(False)
            print("ERROR on creating Labor Status Form/Overload Form" + str(e))

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
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    positionDict = {}
    for position in positions:
        positionDict[position.POSN_CODE] = {"position": position.POSN_TITLE, "WLS":position.WLS}
    return json.dumps(positionDict)

@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>", methods=["POST"])
@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>/<isOneLSF>", methods=["GET"])
def checkForPrimaryPosition(termCode, student, isOneLSF=None):
    """ Checks if a student has a primary supervisor (which means they have primary position) in the selected term. """
    print("before rsp")
    rsp = (request.data).decode("utf-8")  # This turns byte data into a string
    print("after rsp/before rspFunctional")
    rspFunctional = json.loads(rsp)
    print("after rspFunctional")
    term = Term.get(Term.termCode == termCode)
    positions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.studentSupervisee == student)
    isMoreLSF_dict = {}
    if isOneLSF != None:
        isMoreLSF_dict["Status"] = True # student does not have any previous lsf's
        if len(list(positions)) > 1: # If student has one or more than one lsf
            isMoreLSF_dict["Status"] = False
            for item in positions:
                isMoreLSF_dict["primarySupervisorName"] = item.supervisor.FIRST_NAME + " " + item.supervisor.LAST_NAME
                isMoreLSF_dict["studentName"] = item.studentSupervisee.FIRST_NAME + " " + item.studentSupervisee.LAST_NAME
        return jsonify(isMoreLSF_dict)

    try:
        lastPrimaryPosition = FormHistory.select().join_from(FormHistory, LaborStatusForm).where(FormHistory.formID.termCode == termCode, FormHistory.formID.studentSupervisee == student, FormHistory.historyType == "Labor Status Form", FormHistory.formID.jobType == "Primary").order_by(FormHistory.formHistoryID.desc()).get()
    except DoesNotExist:
        lastPrimaryPosition = None

    if not lastPrimaryPosition:
        approvedRelease = None
    else:
        try:
            approvedRelease = FormHistory.select().where(FormHistory.formID == lastPrimaryPosition.formID, FormHistory.historyType == "Labor Release Form", FormHistory.status == "Approved").order_by(FormHistory.formHistoryID.desc()).get()
        except DoesNotExist:
            approvedRelease = None

    finalStatus = ""
    if not term.isBreak:
        if lastPrimaryPosition and not approvedRelease:
            if rspFunctional == "Primary":
                if lastPrimaryPosition.status.statusName == "Denied":
                    finalStatus = "hire"
                else:
                    finalStatus = "no hire"
            else:
                if lastPrimaryPosition.status.statusName == "Approved" or lastPrimaryPosition.status.statusName == "Approved Reluctantly":
                    finalStatus = "hire"
                else:
                    finalStatus = "no hire for secondary"
        elif lastPrimaryPosition and approvedRelease:
            if rspFunctional == "Primary":
                finalStatus = "hire"
            else:
                finalStatus = "no hire for secondary"
        else:
            if rspFunctional == "Primary":
                finalStatus = "hire"
            else:
                finalStatus = "no hire for secondary"
    else:
        finalStatus = "hire"
    return json.dumps(finalStatus)

def checkForSecondLSFBreak(termCode, student, isOneLSF=None):
    positions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.studentSupervisee == student)
    isMoreLSF_dict = {}
    storeLsfFormsID = []
    if isOneLSF != None:
        if len(list(positions)) >= 1: # If student has one or more than one lsf
            isMoreLSF_dict["ShowModal"] = True # show modal when the student has one or more than one lsf
            if len(list(positions)) == 1: # if there is only one labor status form then send email to the supervisor and student
                laborStatusFormID = positions[0].laborStatusFormID
                formHistoryID = FormHistory.get(FormHistory.formID == laborStatusFormID)
                isMoreLSF_dict["Status"] = True
                isMoreLSF_dict["formHistoryID"] = formHistoryID.formHistoryID
            else: # if there are more lsfs then send email to student, supervisor and all previous supervisors
                isMoreLSF_dict["Status"] = False
                for item in positions: # add all the previous lsf ID's
                    storeLsfFormsID.append(item.laborStatusFormID) # store all of the previous labor status forms for break
                laborStatusFormID = storeLsfFormsID.pop() #save all the previous lsf ID's except the one currently created. Pop removes the one created right now.
                formHistoryID = FormHistory.get(FormHistory.formID == laborStatusFormID)
                isMoreLSF_dict['formHistoryID'] = formHistoryID.formHistoryID
                isMoreLSF_dict["lsfFormID"] = storeLsfFormsID
        else:
            #
            isMoreLSF_dict["ShowModal"] = False # Do not show the modal when there's not previous lsf
            isMoreLSF_dict["Status"] = True # student does not have any previous lsf's.
    return json.dumps(isMoreLSF_dict)

@main_bp.route("/laborstatusform/getcompliance/<department>", methods=["GET"])
def checkCompliance(department):
    """ Gets the compliance status of a department. """
    depts = Department.select().where(Department.DEPT_NAME == department)
    deptDict = {}
    for dept in depts:
        deptDict['Department'] = {'Department Compliance': dept.departmentCompliance}
    return json.dumps(deptDict)

@main_bp.route("/laborstatusform/checktotalhours/<termCode>/<student>/<weeklyHours>/<contractHours>", methods=["GET"])
def checkTotalHours(termCode, student, weeklyHours, contractHours):
    """ Counts the total number of hours for the student after the new lsf filled. """
    positions = FormHistory.select().join_from(FormHistory, LaborStatusForm).where(FormHistory.formID.termCode == termCode, FormHistory.formID.studentSupervisee == student, FormHistory.historyType == "Labor Status Form", (FormHistory.status == "Approved" or FormHistory.status == "Approved Reluctantly"))
    term = Term.get(Term.termCode == termCode)
    totalHours = 0
    for item in positions:
        formID = item.formID
        releasedForm = FormHistory.select().where(FormHistory.formID == formID, FormHistory.historyType == "Labor Release Form", FormHistory.status == "Approved")
        if not releasedForm:
            if term.isBreak:
                totalHours = totalHours + item.contractHours
            else:
                totalHours = totalHours + item.weeklyHours
    if term.isBreak:
        totalHours = totalHours + int(contractHours)
    else:
        totalHours = totalHours + int(weeklyHours)
    return json.dumps(totalHours)
