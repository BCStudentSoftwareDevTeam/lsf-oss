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


@main_bp.route('/laborstatusform', methods=['GET'])
def laborStatusForm():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    # Logged in
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
                username_index = data['Secondary Supervisor'].find('B0')
                supervisor_username = data['Supervisor'][username_index:]
                d, created = User.get_or_create(username = supervisor_username)
                secondary_supervisor = d.username
                d, created = Department.get_or_create(DEPT_NAME = data['Department'])
                department = d.departmentID
                d, created = Term.get_or_create(termCode = data['Term'])
                term = d.termCode
                integer_hours = int(data['Hours Per Week'])
                lsf = LaborStatusForm.create(termCode = term,
                                             studentSupervisee = student,
                                             primarySupervisor = primary_supervisor ,
                                             department  = department,
                                             secondarySupervisor = secondary_supervisor,
                                             jobType = data['Job Type'],
                                             POSN_TITLE = data['Position'],
                                             startDate = data['Start Date'],
                                             endDate = data['End Date'],
                                             weeklyHours   = integer_hours)
                print("created the form")
            return jsonify({"Success": True})
    except Exception as e:
        print("im here last")
        print(e)
        return jsonify({"Success": False})




#
#     flash("changed")

@main_bp.route("/laborstatusform/getPositions/<department>", methods=['GET'])
def getPositions(department):
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    position_dict = {}
    for position in positions:
        position_dict[position.POSN_CODE] = {"position": position.POSN_TITLE}
    return json.dumps(position_dict)

@main_bp.route("/laborstatusform/getstudents/<termCode>/<student>", methods=["GET"])
def getprimarysupervisor(termCode, student):
    primary_supervisors = LaborStatusForm.select().where(LaborStatusForm.termCode == termCode, LaborStatusForm.jobType == "Primary", LaborStatusForm.studentSupervisee == student)
    primary_supervisor_dict = {}
    for primary_supervisor in primary_supervisors:
        primary_supervisor_dict[str(primary_supervisor.laborStatusFormID)] = {"Primary Supervisor FirstName":primary_supervisor.primarySupervisor.FIRST_NAME,
        "Primary Supervisor LastName": primary_supervisor.primarySupervisor.LAST_NAME, "Primary Supervisor ID":primary_supervisor.primarySupervisor.username}
    return json.dumps(primary_supervisor_dict)
