from app.controllers.admin_routes import *
from app.models.user import User
from app.models.user import *
from app.controllers.admin_routes import admin
from flask import request
from app.login_manager import require_login
from flask import Flask, redirect, url_for, flash, jsonify
from app.models.supervisor import Supervisor
from app.models.student import Student
from app.logic.tracy import Tracy
from app.logic.userInsertFunctions import createUser, createSupervisorFromTracy, createStudentFromTracy

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

@admin.route('/admin/laborAdminSearch', methods=['POST'])
def laborAdminSearch():
    """
    This function takes in the data from the 'Add Labor Admin' select picker, then uses the data to query from the User table and return a list of possible options
    to populate the select picker.
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        userList = []
        tracySupervisors = Tracy().getSupervisorsFromUserInput(rsp)
        supervisors = []
        tracyStudents = Tracy().getStudentsFromUserInput(rsp)
        students = []
        for user in tracySupervisors:
            try:
                currentUser = User.get(User.Supervisor == user.ID)
                if currentUser.isLaborAdmin == True:
                    pass
                else:
                    supervisors.append(user)
            except Exception as e:
                supervisors.append(user)
        for user in tracyStudents:
            try:
                currentUser = User.get(User.Student == user.ID)
                if currentUser.isLaborAdmin == True:
                    pass
                else:
                    students.append(user)
            except Exception as e:
                students.append(user)
        for i in supervisors:
            username = i.EMAIL.split('@', 1)
            userList.append({'username': username[0],
                            'firstName': i.FIRST_NAME,
                            'lastName': i.LAST_NAME,
                            'type': 'Supervisor'
                            })
        for i in students:
            username = i.STU_EMAIL.split('@', 1)
            userList.append({'username': username[0],
                            'firstName': i.FIRST_NAME,
                            'lastName': i.LAST_NAME,
                            'type': 'Student'
                            })
        return jsonify(userList)
    except Exception as e:
        print('ERROR Loading Non Labor Admins:', e, type(e))
        return jsonify(userList)

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
        try:
            newAdmin = User.get(User.username == newAdmins)
        except Exception as e:
            usertype = Tracy().checkStudentOrSupervisor(newAdmins)
            supervisor = student = None
            if usertype == "Student":
                student = createStudentFromTracy(newAdmins)
            else:
                supervisor = createSupervisorFromTracy(newAdmins)
            newAdmin = createUser(newAdmins, student=student, supervisor=supervisor)
        newAdmin.isLaborAdmin = 1
        newAdmin.save()
        if newAdmin.Student:
            message = "{0} {1} has been added as a Labor Admin".format(newAdmin.Student.FIRST_NAME, newAdmin.Student.LAST_NAME)
        elif newAdmin.Supervisor:
            message = "{0} {1} has been added as a Labor Admin".format(newAdmin.Supervisor.FIRST_NAME, newAdmin.Supervisor.LAST_NAME)
        flash(message, "success")

def removeLaborAdmin():
    if request.form.get('removeAdmin') != "":
        user = User.get(User.username == request.form.get('removeAdmin'))   #this is taking the name in the select tag
        user.isLaborAdmin = 0
        user.save()
        if user.Student:
            message = "{0} {1} has been removed as a Labor Admin".format(user.Student.FIRST_NAME, user.Student.LAST_NAME)
        elif user.Supervisor:
            message = "{0} {1} has been removed as a Labor Admin".format(user.Supervisor.FIRST_NAME, user.Supervisor.LAST_NAME)
        flash(message, "danger")

def addFinancialAdmin():
    if request.form.get('addFinancialAidAdmin') != "":
        newFinAidAdmins = request.form.get('addFinancialAidAdmin')
        newFinAidAdmin = User.get(User.username == newFinAidAdmins)
        newFinAidAdmin.isFinancialAidAdmin = 1
        newFinAidAdmin.save()
        message = "{0} {1} has been added as a Financial Aid Admin".format(newFinAidAdmin.Supervisor.FIRST_NAME, newFinAidAdmin.Supervisor.LAST_NAME)
        flash(message, "success")

def removeFinancialAdmin():
    if request.form.get('removeFinancialAidAdmin') != "":
        userFinAid = User.get(User.username == request.form.get('removeFinancialAidAdmin'))
        userFinAid.isFinancialAidAdmin = 0
        userFinAid.save()
        message = "{0} {1} has been removed as a Financial Aid Admin".format(userFinAid.Supervisor.FIRST_NAME, userFinAid.Supervisor.LAST_NAME)
        flash(message, "danger")

def addSAASAdmin():
    if request.form.get('addSAASAdmin') != "":
        newSaasAdmins = request.form.get('addSAASAdmin')
        newSaasAdmin = User.get(User.username == newSaasAdmins)
        newSaasAdmin.isSaasAdmin = 1
        newSaasAdmin.save()
        message = "{0} {1} has been added as a SAAS Admin".format(newSaasAdmin.Supervisor.FIRST_NAME, newSaasAdmin.Supervisor.LAST_NAME)
        flash(message, "success")

def removeSAASAdmin():
    if request.form.get('removeSAASAdmin') != "":
        userSaas = User.get(User.username == request.form.get('removeSAASAdmin'))
        userSaas.isSaasAdmin = 0
        userSaas.save()
        message = "{0} {1} has been removed as a SAAS Admin".format(userSaas.Supervisor.FIRST_NAME, userSaas.Supervisor.LAST_NAME)
        flash(message, "danger")
