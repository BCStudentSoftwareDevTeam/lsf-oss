from app.controllers.admin_routes import *
from app.models.user import *
from app.login_manager import require_login
from app.controllers.admin_routes import admin
from app.controllers.errors_routes.handlers import *
#from app.models.manageDepartments import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import*
from app.models.Tracy.stuposn import *
from app.models.department import *
from flask import request
from flask import jsonify

@admin.route('/admin/manageDepartments', methods=['GET'])
# @login_required
def manage_departments():
    """
    Updates the Labor Status Forms database with any new departments in the Tracy database on page load.
    Returns the departments to be used in the HTML for the manage departments page.
    """
    current_user = require_login()
    if not current_user:
        render_template("errors/403.html")
    if not current_user.isLaborAdmin:
        render_template("errors/403.html")

    users = User.select()
    departmentTracy = STUPOSN.select(STUPOSN.DEPT_NAME).distinct()
    # tracyDepartmentList = []
    for dept in departmentTracy:
        d, created = Department.get_or_create(DEPT_NAME = dept.DEPT_NAME)
        d.ACCOUNT = dept.ACCOUNT
        d.ORG = dept.ORG
        d.save()
    department = Department.select()
    return render_template( 'admin/manageDepartments.html',
    title = ("Manage departments"),
    username = users,
    department = department)


@admin.route('/admin/complianceStatus', methods=['POST'])
def complianceStatusCheck():
    """
    This function changes the compliance status in the database for labor status forms.  It works in collaboration with the ajax call in manageDepartments.js
    """
    try:
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        if rsp:
            department = Department.get(int(rsp['deptName']))
            department.departmentCompliance = not department.departmentCompliance
            department.save()
            return jsonify({"Success": True})
    except Exception as e:
        #print(e)
        return jsonify({"Success": False})
