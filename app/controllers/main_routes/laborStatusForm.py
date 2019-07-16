from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.department import *
from app.models.Tracy.stuposn import STUPOSN
from flask import json
from flask import request

@main_bp.route("/laborstatusform/getPositions/<department>", methods=['GET'])
def getPositions(department):
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    position_dict = {}
    for position in positions:
        position_dict[position.POSN_CODE] = {"position": position.POSN_TITLE}
    return json.dumps(position_dict)

@main_bp.route('/laborstatusform', methods=['GET', 'POST'])
# @login_required
def laborStatusForm():

    username = load_user('heggens')  #FIXME Hardcoding users is bad
    forms = LaborStatusForm.select()
    students = STUDATA.select().order_by(STUDATA.FIRST_NAME.asc()) # getting student names from TRACY
    terms = Term.select().where(Term.termState == "open") # changed to term state, open, closed, inactive
    staffs = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # getting supervisors from TRACY
    departments = STUPOSN.select(STUPOSN.ORG, STUPOSN.DEPT_NAME, STUPOSN.ACCOUNT).distinct()

    # Department.select().order_by(Department.DEPT_NAME.asc()) # getting the names of the departments
    # positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == Department.DEPT_NAME)
    return render_template( 'main/laborStatusForm.html',
				            title=('Labor Status Form'),
                            username = username,#Passing of variables from controller to front
                            forms = forms,
                            students = students,
                            terms = terms,
                            staffs = staffs,
                            departments = departments
                            # positions   = positions
                          )
