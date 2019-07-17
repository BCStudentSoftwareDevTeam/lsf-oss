from app.controllers.admin_routes import *
from app.models.user import User
from app.models.user import *
from app.controllers.admin_routes import admin
from flask import request
from flask import Flask, redirect, url_for

@admin.route('/adminManagement', methods=['GET'])
# @login_required
def admin_Management():
   username = load_user('heggens')
   users = User.select()
   FIRST_NAME = User.select()
   LAST_NAME = User.select()
   EMAIL = User.select()
   CPO = User.select()
   ORG = User.select()
   DEPT_NAME = User.select()
   isLaborAdmin = User.select()
   isFinancialAidAdmin = User.select()
   isSaasAdmin = User.select()
   return render_template( 'admin/adminManagement.html',
                            title=('Admin Management'),
                           username = username,
                           users = users,
                           FIRST_NAME = FIRST_NAME,
                           LAST_NAME = LAST_NAME,
                           EMAIL = EMAIL,
                           CPO = CPO,
                           ORG = ORG,
                           DEPT_NAME = DEPT_NAME,
                           isLaborAdmin = isLaborAdmin,
                           isFinancialAidAdmin = isFinancialAidAdmin,
                           isSaasAdmin = isSaasAdmin
                         )


@admin.route("/adminManagement/userInsert", methods=['POST'])
def manageLaborAdmin():
    if request.form.get("add") == "add":
        addLaborAdmin()
    elif request.form.get("remove") == "remove":
        # print("Hello Ela!!")
        removeLaborAdmin()
    return redirect(url_for('admin.admin_Management'))


def addLaborAdmin():
    newAdmins = request.form.get('addAdmin')
    newAdmin = User.get(User.username == newAdmins)
    newAdmin.isLaborAdmin = 1
    newAdmin.save()

def removeLaborAdmin():
    user = User.get(User.username == request.form.get('removeAdmin'))
    user.isLaborAdmin = 0
    user.save()
