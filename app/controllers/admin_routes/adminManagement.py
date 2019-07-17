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



def manageFinancialAidAdmin():
    if request.form.get("addAid") == "addAid":
        addFinancialAdmin()
    elif request.form.get("removeAid") == "removeAid":
        # print("Hello Ela!!")
        removeFinancialAdmin()
    return redirect(url_for('admin.admin_Management'))


def addFinancialAdmin():
    newFinAidAdmins = request.form.get('addFinancialAidAdmin')
    newFinAidAdmin = User.get(User.username == newFinAidAdmins)
    newFinAidAdmin.isFinancialAidAdmin = 1
    newFinAidAdmin.save()

def removeFinancialAdmin():
    FinAiduser = FinAidUser.get(User.username == request.form.get('removeFinancialAidAdmin'))
    FinAiduser.isFinancialAidAdmin = 0
    FinAiduser.save()



def manageSAASAdmin():
    if request.form.get("addSAAS") == "addSAAS":
        addSAASAdmin()
    elif request.form.get("removeSAAS") == "removeSAAS":
        # print("Hello Ela!!")
        removeSAASAdmin()
    return redirect(url_for('admin.admin_Management'))

def addSAASAdmin():
    newSAASAdmins = request.form.get('addSAASAdmin')
    newSAASAdmin = User.get(User.username == newSAASAdmins)
    newSAASAdmin.isSaasAdmin = 1
    newSAASAdmin.save()

def removeSAASAdmin():
    SAASuser = SAASUser.get(User.username == request.form.get('removeSAASAdmin'))
    SAASuser.isSaasAdmin = 0
    SAASuser.save()
