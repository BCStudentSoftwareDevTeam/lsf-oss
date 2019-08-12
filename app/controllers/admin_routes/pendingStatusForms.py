#from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
#from flask_login import current_user, login_required
from flask import flash, send_file
from app.login_manager import *
from app.controllers.admin_routes import admin
from app.controllers.errors_routes.handlers import *
from app.models.formHistory import *
from app.models.term import Term
from datetime import datetime, date

@admin.route('/admin/pendingStatusForms', methods=['GET', 'POST'])
def pendingForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')


        pending_status_forms = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate)
        print(len(pending_status_forms))
        # Logged in & Admin
        users = User.select()
        return render_template( 'admin/pendingStatusForms.html',
                                title=('Pending Forms'),
                                username=current_user.username,
                                users=users,
                                pending_status_forms = pending_status_forms
                                )
    except:
        render_template('errors/500.html')
# def index():
#     current_user = require_login()
#     #print(current_user)
#     if not current_user:
#         return render_template('errors/403.html')
#
#    pending_status_forms =  formHistory.select().where(LaborStatusForm.supervisor == current_user.username).order_by(LaborStatusForm.endDate.desc())
#     # departmentID = Department.get(Department.DEPT_NAME == current_user.DEPT_NAME)
#     # departmentStudents = LaborStatusForm.select().join(Term).where(LaborStatusForm.termCode.termEnd >= todayDate).where(LaborStatusForm.department == departmentID)
#
#     # pastDepartmentStudents = LaborStatusForm.select().join(Term).where(LaborStatusForm.termCode.termEnd >= todayDate).where(LaborStatusForm.department == departmentID)
#     currentDepartmentStudents = LaborStatusForm.select().join_from(LaborStatusForm, Term).join_from(LaborStatusForm, Department).where(LaborStatusForm.termCode.termEnd >= todayDate).where(LaborStatusForm.department.DEPT_NAME == current_user.DEPT_NAME)
#
#     pastDepartmentStudents = LaborStatusForm.select().join_from(LaborStatusForm, Department).where(LaborStatusForm.department.DEPT_NAME == current_user.DEPT_NAME)
