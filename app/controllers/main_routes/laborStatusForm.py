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
        term = d.termCode
        try:
            lsf = createLaborStatusForm(tracyStudent, studentID, primarySupervisor, department, term, rspFunctional[i])
            status = Status.get(Status.statusName == "Pending")
            d, created = User.get_or_create(username = currentUser.username)
            creatorID = d.UserID
            createOverloadFormAndFormHistory(rspFunctional[i], lsf, creatorID, status) # createOverloadFormAndFormHistory()
            try:
                emailDuringBreak(checkForSecondLSFBreak(term, studentID, "lsf"), term)
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
            datesDict[date.termCode] = {"Term Code": date.termCode,"Start Date":datetime.strftime(start, "%m/%d/%Y")  , "End Date": datetime.strftime(end, "%m/%d/%Y")}
        else:
            datesDict[date.termCode] = {"Term Code": date.termCode, "Start Date":datetime.strftime(start, "%m/%d/%Y")  , "End Date": datetime.strftime(end, "%m/%d/%Y"), "Primary Cut Off": datetime.strftime(primaryCutOff, "%m/%d/%Y")}
    return json.dumps(datesDict)

@main_bp.route("/laborstatusform/getPositions/<department>", methods=['GET'])
def getPositions(department):
    """ Get all of the positions that are in the selected department """
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    positionDict = {}
    for position in positions:
        positionDict[position.POSN_CODE] = {"position": position.POSN_TITLE, "WLS":position.WLS}
    return json.dumps(positionDict)

@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>", methods=["GET"])
@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>/<isOneLSF>", methods=["GET"])
def checkForPrimaryPosition(termCode, student, isOneLSF=None):
    """ Checks if a student has a primary supervisor (which means they have primary position) in the selected term. """
    positions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.studentSupervisee == student)

    isMoreLSF_dict = {}
    if isOneLSF !=None:
        isMoreLSF_dict["Status"] = True # student does not have any previous lsf's
        if len(list(positions)) > 1: # If student has one or more than one lsf
            isMoreLSF_dict["Status"] = False
            for item in positions:
                isMoreLSF_dict["primarySupervisorName"] = item.supervisor.FIRST_NAME + " " + item.supervisor.LAST_NAME
                isMoreLSF_dict["studentName"] = item.studentSupervisee.FIRST_NAME + " " + item.studentSupervisee.LAST_NAME
        return jsonify(isMoreLSF_dict)

    positionsList = []
    for item in positions:
        statusHistory = FormHistory.select().where(FormHistory.formID == item.laborStatusFormID).order_by(FormHistory.formHistoryID.desc()).get()
        positionsDict = {}
        positionsDict["weeklyHours"] = item.weeklyHours
        positionsDict["contractHours"] = item.contractHours
        positionsDict["jobType"] = item.jobType
        positionsDict["POSN_TITLE"] = item.POSN_TITLE
        positionsDict["POSN_CODE"] = item.POSN_CODE
        positionsDict["primarySupervisorName"] = item.supervisor.FIRST_NAME
        positionsDict["primarySupervisorLastName"] = item.supervisor.LAST_NAME
        positionsDict["positionStatus"] = statusHistory.status.statusName
        positionsDict["positionHistory"] = statusHistory.historyType.historyTypeName
        positionsList.append(positionsDict)
    return json.dumps(positionsList) #json.dumps(primaryPositionsDict)

def checkForSecondLSFBreak(termCode, student, isOneLSF=None):
    positions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.studentSupervisee == student)
    isMoreLSF_dict = {}
    storeLsfFormsID = []
    if isOneLSF != None:
        if len(list(positions)) >= 1 : # If student has one or more than one lsf
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
