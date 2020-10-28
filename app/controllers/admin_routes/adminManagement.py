from app.controllers.admin_routes import *
from app.models.user import User, DoesNotExist
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
        if currentUser.student: # logged in as a student
            return redirect('/laborHistory/' + currentUser.student.ID)
        elif currentUser.supervisor:
            return render_template('errors/403.html'), 403

    users = User.select()
    return render_template( 'admin/adminManagement.html',
                            title=('Admin Management'),
                            users = users
                         )

@admin.route('/admin/adminSearch', methods=['POST'])
def adminSearch():
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
        for supervisor in tracySupervisors:
            try:
                existingUser = User.get(User.supervisor == supervisor.ID)
                if existingUser.isLaborAdmin:
                    pass
                else:
                    supervisors.append(supervisor)
            except DoesNotExist as e:
                supervisors.append(supervisor)
        for student in tracyStudents:
            try:
                existingUser = User.get(User.student == student.ID)
                if existingUser.isLaborAdmin:
                    pass
                else:
                    students.append(student)
            except DoesNotExist as e:
                students.append(student)
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
    except DoesNotExist as e:
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
    if user.student:
        message = "{0} {1} has been {2} as a {3} Admin".format(user.student.FIRST_NAME, user.student.LAST_NAME, action, adminType)
    elif user.supervisor:
        message = "{0} {1} has been {2} as a {3} Admin".format(user.supervisor.FIRST_NAME, user.supervisor.LAST_NAME, action, adminType)

    if action == 'added':
        flash(message, "success")
    elif action == 'removed':
        flash(message, "danger")
