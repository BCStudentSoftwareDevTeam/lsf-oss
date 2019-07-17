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
from flask import flash

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
        print(dept.DEPT_NAME)
        d, created = Department.get_or_create(DEPT_NAME = dept.DEPT_NAME)
        print(created)
        print("After get/Create", d.DEPT_NAME)
        d.ACCOUNT = dept.ACCOUNT
        d.ORG = dept.ORG
        d.save()
        print("D saved", d.ORG)
    # print(tracyDepartmentList)
    #
    # department = Department.select()
    # lsfDepartmentList = []
    # lsfDepartmentIDlist = []
    # for n in department:
    #     #print(n.DEPT_NAME)
    #     lsfDepartmentList.append(n.DEPT_NAME)
    #     lsfDepartmentIDlist.append(n.departmentID)
    # print(lsfDepartmentList)
    # print(lsfDepartmentIDlist)
    #
    # currentMaxID = max(lsfDepartmentIDlist)
    # print(currentMaxID)
    # for dept in tracyDepartmentList:
    #     if dept in lsfDepartmentList:
    #         print(str(dept) + " is already in the database")
    #     else:
    #         newDept = STUPOSN.select(STUPOSN.ACCOUNT, STUPOSN.ORG).distinct().where(STUPOSN.DEPT_NAME == dept)
    #         currentMax += 1
    #         for k in newDept:
    #             Department.create(departmentID = currentMax, DEPT_NAME = dept, ACCOUNT = k.ACCOUNT, ORG = k.ORG, departmentCompliance = True)
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
    #print("Starting compliance changer")
    try:
        #print("Get request")
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        #print(rsp)
        if rsp:
            #print("Getting department name", rsp['deptName'])
            #print(type(rsp['deptName']))
            department = Department.get(int(rsp['deptName']))
            #print(department)
            department.departmentCompliance = not department.departmentCompliance
            department.save()
            flash("Department compliance changed")
            #print("worked")
            return jsonify({"Success": True})
    except Exception as e:
        #print(e)
        return jsonify({"Success": False})
