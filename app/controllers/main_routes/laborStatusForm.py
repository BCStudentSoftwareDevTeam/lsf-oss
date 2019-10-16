from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.status import *
from app.models.laborStatusForm import *
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
    try:
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        if rsp:
            for i in rsp:
                print(i)
                wlsIndexStart = data['Position'].find('(')
                wlsIndexEnd = data['Position'].find(')')
                wls = data['Position'][wlsIndexStart + 1 : wlsIndexEnd]
                bnumberIndex = data['Student'].find('B0')
                studentBnumber = data['Student'][bnumberIndex:]
                d, created = Student.get_or_create(ID = studentBnumber)
                student = d.ID
                d, created = User.get_or_create(UserID = data['Supervisor'])
                primarySupervisor = d.UserID
                d, created = Department.get_or_create(DEPT_NAME = data['Department'])
                department = d.departmentID
                d, created = Term.get_or_create(termCode = data['Term'])
                term = d.termCode
                start = data['Start Date']
                startDate = datetime.strptime(start, "%m/%d/%Y").strftime('%Y-%m-%d')
                endDate = datetime.strptime(end, "%m/%d/%Y").strftime('%Y-%m-%d')
                lsf = LaborStatusForm.create(termCode = term,
                                             studentSupervisee = student,
                                             supervisor = primarySupervisor,
                                             department  = department,
                                             jobType = data['Job Type'],
                                             WLS = data['WLS'],
                                             POSN_TITLE = position,
                                             POSN_CODE = data['Position Code'],
                                             contractHours = data.get('Contract Hours', None),
                                             weeklyHours   = data.get('Hours Per Week', None),
                                             startDate = startDate,
                                             endDate = endDate,
                                             supervisorNotes = data.get('Supervisor Notes', None)
                                             )

                historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Status Form")
                status = Status.get(Status.statusName == "Pending")
                formHistroy = FormHistory.create( formID = lsf.laborStatusFormID,
                                                  historyType = historyType.historyTypeName,
                                                  createdBy   = cfg['user']['debug'],
                                                  createdDate = date.today(),
                                                  status      = status.statusName)
            flash("Labor Status Form(s) has been created.", "success")
            return jsonify({"Success": True})
    except Exception as e:
        flash("An error occured.", "danger")
        print("ERROR: " + str(e))
        return jsonify({"Success": False})

@main_bp.route("/laborstatusform/getDate/<termcode>", methods=['GET'])
def getDates(termcode):
    """ Get the start and end dates of the selected term. """
    dates = Term.select().where(Term.termCode == termcode)
    datesDict = {}
    for date in dates:
        start = date.termStart
        end  = date.termEnd
        datesDict[date.termCode] = {"Start Date":datetime.strftime(start, "%m/%d/%Y")  , "End Date": datetime.strftime(end, "%m/%d/%Y")}
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
    print("Inside the Controller")
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
    # print(positionsList)
    return json.dumps(positionsList) #json.dumps(primaryPositionsDict)

@main_bp.route("/laborstatusform/getcompliance/<department>", methods=["GET"])
def checkCompliance(department):
    """ Gets the compliance status of a department. """
    depts = Department.select().where(Department.DEPT_NAME == department)
    deptDict = {}
    for dept in depts:
        deptDict['Department'] = {'Department Compliance': dept.departmentCompliance}
    return json.dumps(deptDict)
