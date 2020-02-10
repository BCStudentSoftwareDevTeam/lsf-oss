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

@main_bp.route('/laborstatusform', methods=['GET'])
@main_bp.route('/laborstatusform/<laborStatusKey>', methods=['GET'])
def laborStatusForm(laborStatusKey = None):
    """ Render labor Status Form, and pre-populate LaborStatusForm page with the correct information when redirected from Labor History."""
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html')
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
                            departments = departments)

@main_bp.route('/laborstatusform/userInsert', methods=['POST'])
def userInsert():
    """ Create labor status form. Create labor history form."""
    rsp = (request.data).decode("utf-8")  # This turns byte data into a string
    rspFunctional = json.loads(rsp)
    all_forms = []
    for i in range(len(rspFunctional)):
        tracyStudent = STUDATA.get(ID = rspFunctional[i]['stuBNumber']) #Gets student info from Tracy
        #Tries to get a student with the followin information from the database
        #if the student doesn't exist, it tries to create a student with that same information
        try:
            d, created = Student.get_or_create(ID = tracyStudent.ID,
                                                FIRST_NAME = tracyStudent.FIRST_NAME,
                                                LAST_NAME = tracyStudent.LAST_NAME,
                                                CLASS_LEVEL = tracyStudent.CLASS_LEVEL,
                                                ACADEMIC_FOCUS = tracyStudent.ACADEMIC_FOCUS,
                                                MAJOR = tracyStudent.MAJOR,
                                                PROBATION = tracyStudent.PROBATION,
                                                ADVISOR = tracyStudent.ADVISOR,
                                                STU_EMAIL = tracyStudent.STU_EMAIL,
                                                STU_CPO = tracyStudent.STU_CPO,
                                                LAST_POSN = tracyStudent.LAST_POSN,
                                                LAST_SUP_PIDM = tracyStudent.LAST_SUP_PIDM)
        except Exception as e:
            print("ERROR: ", e)
            d, created = Student.get(ID = tracyStudent.ID)
        student = d.ID
        d, created = User.get_or_create(UserID = rspFunctional[i]['stuSupervisorID'])
        primarySupervisor = d.UserID
        d, created = Department.get_or_create(DEPT_NAME = rspFunctional[i]['stuDepartment'])
        department = d.departmentID
        d, created = Term.get_or_create(termCode = rspFunctional[i]['stuTermCode'])
        term = d.termCode
        # Changes the dates into the appropriate format for the table
        startDate = datetime.strptime(rspFunctional[i]['stuStartDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
        endDate = datetime.strptime(rspFunctional[i]['stuEndDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
        try:
            lsf = LaborStatusForm.create(termCode_id = term,
                                         studentSupervisee_id = student,
                                         supervisor_id = primarySupervisor,
                                         department_id  = department,
                                         jobType = rspFunctional[i]["stuJobType"],
                                         WLS = rspFunctional[i]["stuWLS"],
                                         POSN_TITLE = rspFunctional[i]["stuPosition"],
                                         POSN_CODE = rspFunctional[i]["stuPositionCode"],
                                         contractHours = rspFunctional[i].get("stuContractHours", None),
                                         weeklyHours   = rspFunctional[i].get("stuWeeklyHours", None),
                                         startDate = startDate,
                                         endDate = endDate,
                                         supervisorNotes = rspFunctional[i]["stuNotes"]
                                         )
            if rspFunctional[i].get("isItOverloadForm") == "True":
                historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form")
            else:
                historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Status Form")
            status = Status.get(Status.statusName == "Pending")
            d, created = User.get_or_create(username = cfg['user']['debug'])
            creatorID = d.UserID
            formHistory = FormHistory.create( formID = lsf.laborStatusFormID,
                                              historyType = historyType.historyTypeName,
                                              createdBy   = creatorID,
                                              createdDate = date.today(),
                                              status      = status.statusName)

            newLaborOverloadForm = OverloadForm.create( overloadReason = "None",
                                                        financialAidApproved = None,
                                                        financialAidApprover = None,
                                                        financialAidReviewDate = None,
                                                        SAASApproved = None,
                                                        SAASApprover = None,
                                                        SAASReviewDate = None,
                                                        laborApproved = None,
                                                        laborApprover = None,
                                                        laborReviewDate = None)
            historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form")
            status = Status.get(Status.statusName == "Pending")
            d, created = User.get_or_create(username = cfg['user']['debug'])
            creatorID = d.UserID
            if(rspFunctional[i]["stuTotalHours"]) != None:
                if (rspFunctional[i]["stuTotalHours"] > 15) and (rspFunctional[i]["stuJobType"] == "Secondary"):
                    formOverload = FormHistory.create( formID = lsf.laborStatusFormID,
                                                      historyType = historyType.historyTypeName,
                                                      overloadForm = newLaborOverloadForm.overloadFormID,
                                                      createdBy   = creatorID,
                                                      createdDate = date.today(),
                                                      status      = status.statusName)
                    email = emailHandler(formOverload.formHistoryID)
                    email.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(formOverload.formHistoryID))
            all_forms.append(True)
        except Exception as e:
            all_forms.append(False)
            print("ERROR: " + str(e))

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
def checkForPrimaryPosition(termCode, student):
    """ Checks if a student has a primary supervisor (which means they have primary position) in the selected term. """
    positions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.studentSupervisee == student)
    positionsList = []
    for item in positions:
        positionsDict = {}
        positionsDict["weeklyHours"] = item.weeklyHours
        positionsDict["contractHours"] = item.contractHours
        positionsDict["jobType"] = item.jobType
        positionsDict["POSN_TITLE"] = item.POSN_TITLE
        positionsDict["POSN_CODE"] = item.POSN_CODE
        positionsDict["primarySupervisorName"] = item.supervisor.FIRST_NAME
        positionsDict["primarySupervisorLastName"] = item.supervisor.LAST_NAME
        # positionsDict["primarySupervisorUserName"] = item.supervisor.username #Passes Primary Supervisor's username if necessary
        positionsList.append(positionsDict)
    return json.dumps(positionsList) #json.dumps(primaryPositionsDict)

@main_bp.route("/laborstatusform/getcompliance/<department>", methods=["GET"])
def checkCompliance(department):
    """ Gets the compliance status of a department. """
    depts = Department.select().where(Department.DEPT_NAME == department)
    deptDict = {}
    for dept in depts:
        deptDict['Department'] = {'Department Compliance': dept.departmentCompliance}
    return json.dumps(deptDict)
