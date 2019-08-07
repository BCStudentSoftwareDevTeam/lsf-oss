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
@main_bp.route('/laborstatusform/<formID>', methods=['GET'])
def laborStatusForm(formID = None):
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template('errors/403.html')
    # Logged in
    wls = STUPOSN.select(STUPOSN.WLS).distinct()
    posnCode = STUPOSN.select(STUPOSN.POSN_CODE).distinct()
    # forms = LaborStatusForm.select()
    students = STUDATA.select().order_by(STUDATA.FIRST_NAME.asc()) # getting student names from TRACY
    terms = Term.select().where(Term.termState == "open") # changed to term state, open, closed, inactive
    staffs = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # getting supervisors from TRACY
    departments = STUPOSN.select(STUPOSN.ORG, STUPOSN.DEPT_NAME, STUPOSN.ACCOUNT).distinct() # getting deparmtent names from TRACY
    if formID != None:
        forms = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formID)
    else:
        forms = None
    return render_template( 'main/laborStatusForm.html',
				            title=('Labor Status Form'),
                            username = currentUser,
                            forms = forms,
                            students = students,
                            terms = terms,
                            staffs = staffs,
                            departments = departments)

@main_bp.route('/laborstatusform/userInsert', methods=['POST'])
def userInsert():
    try:
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        if rsp:
            for data in rsp.values():
                wlsIndexStart = data['Position'].find('(')
                wlsIndexEnd = data['Position'].find(')')
                wls = data['Position'][wlsIndexStart + 1 : wlsIndexEnd]
                bnumberIndex = data['Student'].find('B0')
                studentBnumber = data['Student'][bnumberIndex:]
                d, created = Student.get_or_create(ID = studentBnumber)
                student = d.ID
                d, created = User.get_or_create(username = data['Supervisor'])
                primarySupervisor = d.username
                d, created = Department.get_or_create(DEPT_NAME = data['Department'])
                department = d.departmentID
                d, created = Term.get_or_create(termCode = data['Term'])
                term = d.termCode
                start = data['Start Date']
                startDate = datetime.strptime(start, "%m/%d/%Y").strftime('%Y-%m-%d')
                end = data['End Date']
                endDate = datetime.strptime(end, "%m/%d/%Y").strftime('%Y-%m-%d')
                lsf = LaborStatusForm.create(termCode = term,
                                             studentSupervisee = student,
                                             supervisor = primarySupervisor,
                                             department  = department,
                                             jobType = data['Job Type'],
                                             WLS = wls,
                                             POSN_TITLE = data['Position'],
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
        return jsonify({"Success": False})

@main_bp.route("/laborstatusform/getDate/<termcode>", methods=['GET'])
def getDates(termcode):
    dates = Term.select().where(Term.termCode == termcode)
    datesDict = {}
    for date in dates:
        start = date.termStart
        end  = date.termEnd
        datesDict[date.termCode] = {"Start Date":datetime.strftime(start, "%m/%d/%Y")  , "End Date": datetime.strftime(end, "%m/%d/%Y")}
    return json.dumps(datesDict)

@main_bp.route("/laborstatusform/getPositions/<department>", methods=['GET'])
def getPositions(department):
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    positionDict = {}
    for position in positions:
        positionDict[position.POSN_CODE] = {"position": position.POSN_TITLE, "WLS":position.WLS}
    return json.dumps(positionDict)

@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>", methods=["GET"])
def checkForPrimaryPosition(termCode, student):
    primaryPositions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.jobType == "Primary", LaborStatusForm.studentSupervisee == student)
    primaryPositionsDict = {}
    for primary_position in primaryPositions:
        primaryPositionsDict["PrimarySupervisor"] = {"Primary Supervisor FirstName":primary_position.supervisor.FIRST_NAME,
        "Primary Supervisor LastName": primary_position.supervisor.LAST_NAME, "Primary Supervisor ID":primary_position.supervisor.username}
    return json.dumps(primaryPositionsDict)

@main_bp.route("/laborstatusform/gethours/<termCode>/<student>", methods=["GET"])
def checkForTotalHours(termCode, student):
    hours = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.studentSupervisee == student)
    total = 0
    hoursDict = {}
    for hour in hours:
        total += hour.weeklyHours
    hoursDict["weeklyHours"] = {"Total Weekly Hours": total}
    return json.dumps(hoursDict)

@main_bp.route("/laborstatusform/getcompliance/<department>", methods=["GET"])
def checkCompliance(department):
    depts = Department.select().where(Department.DEPT_NAME == department)
    deptDict = {}
    for dept in depts:
        deptDict['Department'] = {'Department Compliance': dept.departmentCompliance}
    return json.dumps(deptDict)
