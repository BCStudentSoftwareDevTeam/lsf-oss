from app.controllers.admin_routes import *
from app.models.user import User
from app.models.user import *
from app.controllers.admin_routes import admin
from flask import request
from app.login_manager import require_login
from flask import Flask, redirect, url_for, flash
from app.models.supervisor import Supervisor

@admin.route('/admin/adminManagement', methods=['GET'])
# @login_required
def admin_Management():
# username = load_user('heggens')
    currentUser = require_login()
    if not currentUser:                    # Not logged in
        return render_template('errors/403.html'), 403
    if not currentUser.isLaborAdmin:       # Not an admin
        if currentUser.Student: # logged in as a student
            return redirect('/laborHistory/' + currentUser.Student.ID)
        elif currentUser.Supervisor:
            return render_template('errors/403.html'), 403

    users = User.select()
    return render_template( 'admin/adminManagement.html',
                            title=('Admin Management'),
                            users = users
                         )


@admin.route("/adminManagement/userInsert", methods=['POST'])
def manageLaborAdmin():
    if request.form.get("addAdmin") != "":
        newAdmin = getUser('addAdmin')
        addAdmin(newAdmin, 'labor')
        flashMassage(newAdmin, 'added', 'Labor')

    elif request.form.get("removeAdmin") != "":
        oldAdmin = getUser('removeAdmin')
        removeAdmin(oldAdmin, 'labor')
        flashMassage(oldAdmin, 'removed', 'Labor')

    elif request.form.get("addFinancialAidAdmin") != "":
        newAdmin = getUser('addFinancialAidAdmin')
        addAdmin(newAdmin, 'finAid')
        flashMassage(newAdmin, 'added', 'Financial Aid')

    elif request.form.get("removeFinancialAidAdmin") != "":
        oldAdmin = getUser('removeFinancialAidAdmin')
        removeAdmin(oldAdmin, 'finAid')
        flashMassage(oldAdmin, 'removed', 'Financial Aid')

    elif request.form.get("addSAASAdmin") != "":
        newAdmin = getUser('addSAASAdmin')
        addAdmin(newAdmin, 'saas')
        flashMassage(newAdmin, 'added', 'SAAS')

    elif request.form.get("removeSAASAdmin") != "":
        oldAdmin = getUser('removeSAASAdmin')
        removeAdmin(oldAdmin, 'saas')
        flashMassage(oldAdmin, 'removed', 'SAAS')

    return redirect(url_for('admin.admin_Management'))

def getUser(selectpickerID):
    username = request.form.get(selectpickerID)
    user = User.get(User.username == username)
    return user

def addAdmin(newAdmin, adminType):
    if adminType == 'labor':
        newAdmin.isLaborAdmin = 1
    if adminType == 'finAid':
        newAdmin.isFinancialAidAdmin = 1
    if adminType == 'saas':
        newAdmin.isSaasAdmin = 1
    newAdmin.save()

def removeAdmin(oldAdmin, adminType):
    if adminType == 'labor':
        oldAdmin.isLaborAdmin = 0
    if adminType == 'finAid':
        oldAdmin.isFinancialAidAdmin = 0
    if adminType == 'saas':
        oldAdmin.isSaasAdmin = 0
    oldAdmin.save()

def flashMassage(user, action, adminType):
    if user.Student:
        message = "{0} {1} has been {2} as a {3} Admin".format(user.Student.FIRST_NAME, user.Student.LAST_NAME, action, adminType)
    elif user.Supervisor:
        message = "{0} {1} has been {2} as a {3} Admin".format(user.Supervisor.FIRST_NAME, user.Supervisor.LAST_NAME, action, adminType)

    if action == 'added':
        flash(message, "success")
    elif action == 'removed':
        flash(message, "danger")
