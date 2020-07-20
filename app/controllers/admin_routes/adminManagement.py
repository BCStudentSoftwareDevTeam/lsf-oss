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
    if request.form.get("add") == "add" and request.form.get('addAdmin') != "":
        newAdmin = getUser('addAdmin')
        addAdmin(newAdmin, labor='labor')
        flashMassage(newAdmin, 'added', 'Labor')

    elif request.form.get("remove") == "remove" and request.form.get('removeAdmin') != "":
        oldAdmin = getUser('removeAdmin')
        removeAdmin(oldAdmin, labor='labor')
        flashMassage(oldAdmin, 'removed', 'Labor')

    elif request.form.get("addAid") == "addAid" and request.form.get('addFinancialAidAdmin') !="":
        newAdmin = getUser('addFinancialAidAdmin')
        addAdmin(newAdmin, finAid='finAid')
        flashMassage(newAdmin, 'added', 'Financial Aid')

    elif request.form.get("removeAid") == "removeAid" and request.form.get('removeFinancialAidAdmin') != "":
        oldAdmin = getUser('removeFinancialAidAdmin')
        removeAdmin(oldAdmin, finAid='finAid')
        flashMassage(oldAdmin, 'removed', 'Financial Aid')

    elif request.form.get("addSaas") == "addSaas" and request.form.get('addSAASAdmin') != "":
        newAdmin = getUser('addSAASAdmin')
        addAdmin(newAdmin, saas='saas')
        flashMassage(newAdmin, 'added', 'SAAS')

    elif request.form.get("removeSaas") == "removeSaas" and request.form.get('removeSAASAdmin') != "":
        oldAdmin = getUser('removeSAASAdmin')
        removeAdmin(oldAdmin, saas='saas')
        flashMassage(oldAdmin, 'removed', 'SAAS')

    return redirect(url_for('admin.admin_Management'))

def getUser(username):
    username = request.form.get(username)
    user = User.get(User.username == username)
    return user

def addAdmin(newAdmin, labor=None, finAid=None, saas=None):
    if labor:
        newAdmin.isLaborAdmin = 1
    if finAid:
        newAdmin.isFinancialAidAdmin = 1
    if saas:
        newAdmin.isSaasAdmin = 1
    newAdmin.save()

def removeAdmin(oldAdmin, labor=None, finAid=None, saas=None):
    if labor:
        oldAdmin.isLaborAdmin = 0
    if finAid:
        oldAdmin.isFinancialAidAdmin = 0
    if saas:
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
