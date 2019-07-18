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


@main_bp.route('/laborstatusform', methods=['GET', 'POST'])
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
