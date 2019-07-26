from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
from app.models.student import Student
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.department import *
from app.models.Tracy.stuposn import STUPOSN
from flask import json, jsonify
from flask import request
from datetime import datetime
from flask import flash

@main_bp.route('/laborstatusform', methods=['GET'])
def laborStatusForm():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    # Logged in
    wls = STUPOSN.select(STUPOSN.WLS).distinct()
    posn_code = STUPOSN.select(STUPOSN.POSN_CODE).distinct()
    forms = LaborStatusForm.select()
    students = STUDATA.select().order_by(STUDATA.FIRST_NAME.asc()) # getting student names from TRACY
    terms = Term.select().where(Term.termState == "open") # changed to term state, open, closed, inactive
    staffs = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # getting supervisors from TRACY
    departments = STUPOSN.select(STUPOSN.ORG, STUPOSN.DEPT_NAME, STUPOSN.ACCOUNT).distinct() # getting deparmtent names from TRACY
    return render_template( 'main/laborStatusForm.html',
				            title=('Labor Status Form'),
                            username = current_user,
                            forms = forms,
                            students = students,
                            terms = terms,
                            staffs = staffs,
                            departments = departments)

@main_bp.route('/laborstatusform/userInsert', methods=['POST'])
def userInsert():
    print("i'm here 1")
    try:
        print("im here 2")
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        print(rsp)
        print("im here 3")
        if rsp:
            print("Success")
            for data in rsp.values():
                print(data)
                bnumber_index = data['Student'].find('B0')
                student_bnumber = data['Student'][bnumber_index:]
                d, created = Student.get_or_create(ID = student_bnumber)
                student = d.ID
                d, created = User.get_or_create(username = data['Supervisor'])
                primary_supervisor = d.username
                d, created = Department.get_or_create(DEPT_NAME = data['Department'])
                department = d.departmentID
                d, created = Term.get_or_create(termCode = data['Term'])
                term = d.termCode
                integer_hours = int(data['Hours Per Week'])
                start = data['Start Date']
                startdate = datetime.strptime(start, "%m-%d-%Y")
                end = data['End Date']
                enddate = datetime.strptime(end, "%m-%d-%Y")
                lsf = LaborStatusForm.create(termCode = term,
                                             studentSupervisee = student,
                                             supervisor = primary_supervisor ,
                                             department  = department,
                                             jobType = data['Job Type'],
                                             POSN_TITLE = data['Position'],
                                             startDate = startdate,
                                             endDate = enddate,
                                             weeklyHours   = integer_hours)
            return jsonify({"Success": True})
    except Exception as e:
        print("im here last")
        print(e)
        return jsonify({"Success": False})

@main_bp.route("/laborstatusform/getDate/<termcode>", methods=['GET'])
def getdates(termcode):
    dates = Term.select().where(Term.termCode == termcode)
    dates_dict = {}
    for date in dates:
        start = date.termStart
        end  = date.termEnd
        dates_dict[date.termCode] = {"Start Date":datetime.strftime(start, "%m-%d-%Y")  , "End Date": datetime.strftime(end, "%m-%d-%Y")}
    return json.dumps(dates_dict)

@main_bp.route("/laborstatusform/getPositions/<department>", methods=['GET'])
def getPositions(department):
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    position_dict = {}
    for position in positions:
        position_dict[position.POSN_CODE] = {"position": position.POSN_TITLE, "Position Code": position.POSN_CODE, "WLS":position.WLS}
    return json.dumps(position_dict)

@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>", methods=["GET"])
def getprimarysupervisor(termCode, student):
    primary_supervisors = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.jobType == "Primary", LaborStatusForm.studentSupervisee == student)
    primary_supervisor_dict = {}
    for primary_supervisor in primary_supervisors:
        primary_supervisor_dict[str(primary_supervisor.laborStatusFormID)] = {"Primary Supervisor FirstName":primary_supervisor.supervisor.FIRST_NAME,
        "Primary Supervisor LastName": primary_supervisor.supervisor.LAST_NAME, "Primary Supervisor ID":primary_supervisor.supervisor.username}
    print(primary_supervisor_dict)
    return json.dumps(primary_supervisor_dict)
