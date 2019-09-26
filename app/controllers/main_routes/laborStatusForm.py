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
            for data in rsp.values():
# <<<<<<< HEAD
#                 del data['undefined']
#                 print(data)
#                 # wlsIndexStart = data['Position'].find('(')
#                 # position = data['Position'][:wlsIndexStart]
#                 # bnumberIndexStart = data['Student'].find('(')
#                 # bnumberIndexEnd = data['Student'].find(')')
#                 # studentBnumber = data['Student'][bnumberIndexStart + 1: bnumberIndexEnd]
#                 # print(studentBnumber)
#                 # created = Student.select().where(Student.ID == studentBnumber)
#                 # print("Created", created)
#                 # if created:
#                     # print(created)
#                     # student = d.ID
#                 print('supervisor name')
#                 print(data['Supervisor'])
#                 d, created = User.get_or_create(username = data['Supervisor'])
#                 print(d.username)
#                 primarySupervisor = d.username
#                 if not created: # true ( FIXME: 'not' should be removed. It should be 'if created'. I have it there just for checking)
#                     print("Adding user ")
#                     supervisor = STUSTAFF.get(STUSTAFF.PIDM == d.username)
#                     supervisorBnumber = supervisor.ID
#                     supervisorFirstName = supervisor.FIRST_NAME
#                     supervisorLastName = supervisor.LAST_NAME
#                     supervisorCPO = supervisor.CPO
#                     supervisorORG = supervisor.ORG
#                     supervisorPIDM = supervisor.PIDM
#                     print(supervisor)
#                     print(supervisorBnumber)
#                     print(supervisorCPO)
#
#
#                 # d, created = Department.get_or_create(DEPT_NAME = data['Department'])
#                 # department = d.departmentID
#                 # d, created = Term.get_or_create(termCode = data['Term'])
#                 #     term = d.termCode
#                 # else:
#                 #     #Getting data from TRACY if the student is not already in our database
#                 #     print("HELLO")
#                 #     student = STUDATA.select().where(STUDATA.ID == studentBnumber)
#                 #     print(type(student))
#                 #     print("1")
#                 #     print(student)
#                 #     firstName = STUDATA.select(STUDATA.FIRST_NAME).where(STUDATA.ID == studentBnumber).FIRST_NAME
#                 #     lastName = STUDATA.select(STUDATA.LAST_NAME).where(STUDATA.ID == studentBnumber).LAST_NAME
#                 #     classLevel = STUDATA.select(STUDATA.CLASS_LEVEL).where(STUDATA.ID == studentBnumber).CLASS_LEVEL
#                 #     academicFocus = STUDATA.select(STUDATA.ACADEMIC_FOCUS).where(STUDATA.ID == studentBnumber).ACADEMIC_FOCUS
#                 #     major = STUDATA.select(STUDATA.MAJOR).where(STUDATA.ID == studentBnumber).MAJOR
#                 #     probation = STUDATA.select(STUDATA.PROBATION).where(STUDATA.ID == studentBnumber).PROBATION
#                 #     advisor = STUDATA.select(STUDATA.ADVISOR).where(STUDATA.ID == studentBnumber).ADVISOR
#                 #     studentEmail = STUDATA.select(STUDATA.STU_EMAIL).where(STUDATA.ID == studentBnumber).STU_EMAIL
#                 #     studentCPO = STUDATA.select(STUDATA.STU_CPO).where(STUDATA.ID == studentBnumber).STU_CPO
#                 #     lastPosition = STUDATA.select(STUDATA.LAST_POSN).where(STUDATA.ID == studentBnumber).LAST_POSN
#                 #     lastSupervisorPIDM = STUDATA.select(STUDATA.LAST_SUP_PIDM).where(STUDATA.ID == studentBnumber).LAST_SUP_PIDM
#                 #
#                 #     student = Student.create(ID = studentBnumber,
#                 #                             FIRST_NAME = firstName,
#                 #                             LAST_NAME = lastName,
#                 #                             CLASS_LEVEL = classLevel,
#                 #                             ACADEMIC_FOCUS = academicFocus,
#                 #                             MAJOR = major,
#                 #                             PROBATION = probation,
#                 #                             ADVISOR = advisor,
#                 #                             STU_EMAIL = studentEmail,
#                 #                             STU_CPO = studentCPO,
#                 #                             LAST_POSN = lastPosition,
#                 #                             LAST_SUP_PIDM = lastSupervisorPIDM
#                 #                             )
#                 #
#                 #     #Adding the absent data to the Student table
#                 #     # d, created = Student.create(FIRST_NAME = firstName, LAST_name = lastName, CLASS_LEVEL = classLevel)
#                 #     # # d, created = Student.create(LAST_name = lastName)
#                 #     # # d, created = Student.create(CLASS_LEVEL = classLevel)
#                 #     # d, created = Student.create(ACADEMIC_FOCUS = academicFocus)
#                 #     # d, created = Student.create(MAJOR = major)
#                 #     # d, created = Student.create(PROBATION = probation)
#                 #     # d, created = Student.create(ADVISOR = advisor)
#                 #     # d, created = Student.create(STU_EMAIL = studentEmail)
#                 #     # d, created = Student.create(STU_CPO = studentCPO)
#                 #     # d, created = Student.create(LAST_POSN = lastPosition)
#                 #     # d, created = Student.create(LAST_SUP_PIDM = lastSupervisorPIDM)
#                 #
#
#
#                 startIndex = data['Contract Dates'].find(' -')
#                 EndIndex = data['Contract Dates'].find('- ')
#                 start = data['Contract Dates'][:startIndex]
#                 end = data['Contract Dates'][EndIndex+2:]
# =======
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
#>>>>>>> development
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
    primaryPositions = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.jobType == "Primary", LaborStatusForm.studentSupervisee == student)
    primaryPositionsDict = {}
    for primary_position in primaryPositions:
        primaryPositionsDict["PrimarySupervisor"] = {"Primary Supervisor FirstName":primary_position.supervisor.FIRST_NAME,
        "Primary Supervisor LastName": primary_position.supervisor.LAST_NAME, "Primary Supervisor ID":primary_position.supervisor.UserID, "selectedJobType":primary_position.jobType}
    return json.dumps(primaryPositionsDict)

@main_bp.route("/laborstatusform/gethours/<termCode>/<student>", methods=["GET"])
def checkForTotalHours(termCode, student):
    """ Calculates total weekly hours of a student and returns the total. """
    hours = LaborStatusForm.select().where(LaborStatusForm.termCode == int(termCode), LaborStatusForm.studentSupervisee == student)
    total = 0
    hoursDict = {}
    for hour in hours:
        total += hour.weeklyHours
    hoursDict["weeklyHours"] = {"Total Weekly Hours": total}
    return json.dumps(hoursDict)

@main_bp.route("/laborstatusform/getcompliance/<department>", methods=["GET"])
def checkCompliance(department):
    """ Gets the compliance status of a department. """
    depts = Department.select().where(Department.DEPT_NAME == department)
    deptDict = {}
    for dept in depts:
        deptDict['Department'] = {'Department Compliance': dept.departmentCompliance}
    return json.dumps(deptDict)
