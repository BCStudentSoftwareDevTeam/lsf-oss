from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
#from app.models.manageDepartments import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import*
from app.models.department import *
from flask import request

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
    if request.form.get('deptName'): # MAKE SURE IT EQUALS TO THE VALUE OF THE BUTTON
        print(request.form.get('deptName'))
        deptName.complianceStatus =
    #elif request.form.get('deptName'):
    #    request.form['deptName'] == 'inCompliance'

    #deptName = request.form.get("deptName")

#def changeComplianceStatus():
    #if request.form['complianceButton'] == 'inCompliance':
    #    new = request.form.get("")
    #elif request.form['complianceButton'] == 'notInCompliance':
    #    pass
    #pass
