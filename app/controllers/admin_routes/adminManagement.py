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
    if request.form.get("addAdmin"):
        newAdmin = getUser('addAdmin')
        addAdmin(newAdmin, 'labor')
        flashMassage(newAdmin, 'added', 'Labor')

    elif request.form.get("removeAdmin"):
        oldAdmin = getUser('removeAdmin')
        removeAdmin(oldAdmin, 'labor')
        flashMassage(oldAdmin, 'removed', 'Labor')

    elif request.form.get("addFinancialAidAdmin"):
        newAdmin = getUser('addFinancialAidAdmin')
        addAdmin(newAdmin, 'finAid')
        flashMassage(newAdmin, 'added', 'Financial Aid')

    elif request.form.get("removeFinancialAidAdmin"):
        oldAdmin = getUser('removeFinancialAidAdmin')
        removeAdmin(oldAdmin, 'finAid')
        flashMassage(oldAdmin, 'removed', 'Financial Aid')

    elif request.form.get("addSAASAdmin"):
        newAdmin = getUser('addSAASAdmin')
        addAdmin(newAdmin, 'saas')
        flashMassage(newAdmin, 'added', 'SAAS')

    elif request.form.get("removeSAASAdmin"):
        oldAdmin = getUser('removeSAASAdmin')
        removeAdmin(oldAdmin, 'saas')
        flashMassage(oldAdmin, 'removed', 'SAAS')

    return redirect(url_for('admin.admin_Management'))

def getUser(selectpickerID):
    username = request.form.get(selectpickerID)
    try:
        user = User.get(User.username == username)
    except Exception as e:
        usertype = Tracy().checkStudentOrSupervisor(username)
        supervisor = student = None
        if usertype == "Student":
            student = createStudentFromTracy(username)
        else:
            supervisor = createSupervisorFromTracy(username)
        user = createUser(username, student=student, supervisor=supervisor)
    return user

def addAdmin(newAdmin, adminType):
    if adminType == 'labor':
        newAdmin.isLaborAdmin = True
    if adminType == 'finAid':
        newAdmin.isFinancialAidAdmin = True
    if adminType == 'saas':
        newAdmin.isSaasAdmin = True
    newAdmin.save()

def removeAdmin(oldAdmin, adminType):
    if adminType == 'labor':
        oldAdmin.isLaborAdmin = False
    if adminType == 'finAid':
        oldAdmin.isFinancialAidAdmin = False
    if adminType == 'saas':
        oldAdmin.isSaasAdmin = False
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
