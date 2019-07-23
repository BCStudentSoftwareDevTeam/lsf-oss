from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
# from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.department import *
from app.models.Tracy.stuposn import STUPOSN
from flask import json
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

# @main_bp.route('/laborstatusform/userInsert', methods=['POST'])
# def userInsert():
#     print("i'm here 1")
#     try:
#         print("im here 2")
#         rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
#         print(rsp)
#         print("im here 3")
#         if rsp: ### DO STUFF
#             #print("Getting department name", rsp['deptName'])
#             #print(type(rsp['deptName']))
#             department = Department.get(int(rsp['deptName']))
#             #print(department)
#             department.departmentCompliance = not department.departmentCompliance
#             department.save()
#             #print("worked")
#             return jsonify({"Success": True})
#     except Exception as e:
#         print("im here last")
#         print(e)
#         return jsonify({"Success": False})
# def form_submission(request):
#     print("i'm here")
#     student_form = request.form.get("student")
#     supervisor_form = request.form.get("supervisor")
#     department_form = request.form.get("department")
#     term = request.form.get("term")
#     startdate = request.form.get("startdate")
#     enddate = request.form.get("enddate")
#     position = request.form.get("position")
#     contracthours = request.form.get("contracthours")
#     jobtype = request.form.get("jobtype")
#     secondary_supervisor_form = request.form.get("primary_supervisor")
#     student = Student.get_or_create(Student.PIDM == student_form)
#     supervisor = User.get_or_create(User.username == supervisor_form)
#     secondary_supervisor = User.get_or_create(User.username == secondary_supervisor_form)
#     department = Department.get_or_create(Department.departmentID == department_form)
#     lsf = LaborStatusForm.create(termCode == term,
#                                  studentSupervisee == student,
#                                  primarySupervisor == supervisor,
#                                  department  == department,
#                                  secondarySupervisor == secondary_supervisor,
#                                  jobType == jobtype,
#                                  POSN_TITLE == position,
#                                  startDate == startdate,
#                                  endDate == enddate,
#                                  contractHours == contracthours)
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
        "Primary Supervisor LastName": primary_supervisor.primarySupervisor.LAST_NAME}
    return json.dumps(primary_supervisor_dict)
