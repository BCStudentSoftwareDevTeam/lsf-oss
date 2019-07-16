from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
#from app.models.manageDepartments import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import*
from app.models.department import *
from flask import request
from flask import jsonify

@admin.route('/admin/manageDepartments', methods=['GET'])
# @login_required
def manage_departments():
    username = load_user('heggens')
    users = User.select()
    department = Department.select()
    return render_template( 'admin/manageDepartments.html',
    title = ("Manage departments"),
    username = username,
    department = department)


@admin.route('/admin/complianceStatus', methods=['POST'])
#TODO MAKE A FUNCTION
def complianceStatusCheck():
    """
    Placeholder docstring
    """
    print("Starting compliance changer")
    try:
        print("Get request")
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        print(rsp)
        if rsp:
            print("Getting department name", rsp['deptName'])
            print(type(rsp['deptName']))
            department = Department.get(int(rsp['deptName']))
            print(department)
            department.departmentCompliance = not department.departmentCompliance
            department.save()
            print("worked")
            return jsonify({"Success": True})
    except Exception as e:
        print(e)
        return jsonify({"Success": False})
