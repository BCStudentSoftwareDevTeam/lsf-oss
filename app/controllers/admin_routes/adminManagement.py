from app.controllers.admin_routes import *
from app.models.user import User
from app.models.user import *
from app.controllers.admin_routes import admin
from flask import request
from app.login_manager import require_login
from flask import Flask, redirect, url_for, flash

@admin.route('/admin/adminManagement', methods=['GET'])
# @login_required
def admin_Management():
# username = load_user('heggens')
    current_user = require_login()
    if not current_user:                    # Not logged in
        return render_template('errors/403.html')
    if not current_user.isLaborAdmin:       # Not an admin
        if current_user.ID != None: # logged in as a student
            return redirect('/laborHistory/' + current_user.ID)
        else:
            isLaborAdmin = False
            return render_template('errors/403.html',
                                isLaborAdmin = isLaborAdmin)
    else:
        isLaborAdmin = True

    users = User.select()
    return render_template( 'admin/adminManagement.html',
                            title=('Admin Management'),
                           # username = username,
                           isLaborAdmin = isLaborAdmin,
                           users = users
                         )


@admin.route("/adminManagement/userInsert", methods=['POST'])
def manageLaborAdmin():
    if request.form.get("add") == "add":   #this is taking the id in the select tag
        addLaborAdmin()
    elif request.form.get("remove") == "remove":  #this is taking the id in the select tag
        removeLaborAdmin()
    elif request.form.get("addAid") == "addAid":
        addFinancialAdmin()
    elif request.form.get("removeAid") == "removeAid":
        removeFinancialAdmin()
    elif request.form.get("addSaas") == "addSaas":
        addSAASAdmin()
    elif request.form.get("removeSaas") == "removeSaas":
        removeSAASAdmin()
    return redirect(url_for('admin.admin_Management'))

def addLaborAdmin():
    if request.form.get('addAdmin') != "":
        newAdmins = request.form.get('addAdmin')   #this is taking the name in the select tag
        newAdmin = User.get(User.username == newAdmins)
        newAdmin.isLaborAdmin = 1
        newAdmin.save()
        message = "{0} {1} has been added as a Labor Admin".format(newAdmin.FIRST_NAME, newAdmin.LAST_NAME)
        flash(message, "success")

def removeLaborAdmin():
    if request.form.get('removeAdmin') != "":
        user = User.get(User.username == request.form.get('removeAdmin'))   #this is taking the name in the select tag
        user.isLaborAdmin = 0
        user.save()
        message = "{0} {1} has been removed as a Labor Admin".format(user.FIRST_NAME, user.LAST_NAME)
        flash(message, "danger")

def addFinancialAdmin():
    if request.form.get('addFinancialAidAdmin') != "":
        newFinAidAdmins = request.form.get('addFinancialAidAdmin')
        newFinAidAdmin = User.get(User.username == newFinAidAdmins)
        newFinAidAdmin.isFinancialAidAdmin = 1
        newFinAidAdmin.save()
        message = "{0} {1} has been added as a Financial Aid Admin".format(newFinAidAdmin.FIRST_NAME, newFinAidAdmin.LAST_NAME)
        flash(message, "success")

def removeFinancialAdmin():
    if request.form.get('removeFinancialAidAdmin') != "":
        userFinAid = User.get(User.username == request.form.get('removeFinancialAidAdmin'))
        userFinAid.isFinancialAidAdmin = 0
        userFinAid.save()
        message = "{0} {1} has been removed as a Financial Aid Admin".format(userFinAid.FIRST_NAME, userFinAid.LAST_NAME)
        flash(message, "danger")

def addSAASAdmin():
    if request.form.get('addSAASAdmin') != "":
        newSaasAdmins = request.form.get('addSAASAdmin')
        newSaasAdmin = User.get(User.username == newSaasAdmins)
        newSaasAdmin.isSaasAdmin = 1
        newSaasAdmin.save()
        message = "{0} {1} has been added as a SAAS Admin".format(newSaasAdmin.FIRST_NAME, newSaasAdmin.LAST_NAME)
        flash(message, "success")

def removeSAASAdmin():
    if request.form.get('removeSAASAdmin') != "":
        userSaas = User.get(User.username == request.form.get('removeSAASAdmin'))
        userSaas.isSaasAdmin = 0
        userSaas.save()
        message = "{0} {1} has been removed as a SAAS Admin".format(userSaas.FIRST_NAME, userSaas.LAST_NAME)
        flash(message, "danger")
