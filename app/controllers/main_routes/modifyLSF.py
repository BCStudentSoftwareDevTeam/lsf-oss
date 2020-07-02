from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.user import User
from app.logic.tracy import Tracy
from app.models.modifiedForm import *
from flask_bootstrap import bootstrap_find_resource
from app.login_manager import require_login
from datetime import date, datetime
from flask import json, jsonify
from flask import request
from flask import flash
import base64
from app import cfg
from app.logic.emailHandler import*
from app.models.supervisor import Supervisor

@main_bp.route('/modifyLSF/<laborStatusKey>', methods=['GET']) #History modal called it laborStatusKey
def modifyLSF(laborStatusKey):
    ''' This function gets all the form's data and populates the front end with it'''
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    if not current_user.isLaborAdmin:       # Not an admin
        if current_user.Student and not current_user.Supervisor:
            return redirect('/laborHistory/' + current_user.Student.ID)
        elif current_user.Supervisor:
            isLaborAdmin = False
    else:
        isLaborAdmin = True
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)
    form = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
    #Step 2: get prefill data from said form, then the data that populates dropdowns for supervisors and position
    prefillstudent = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME+" ("+form.studentSupervisee.ID+")"
    prefillsupervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
    prefillsupervisorID = form.supervisor.PIDM
    superviser_id = form.supervisor.ID
    prefilldepartment = form.department.DEPT_NAME
    prefillposition = form.POSN_TITLE #+ " " +"("+ form.WLS + ")"
    prefilljobtype = form.jobType
    prefillterm = form.termCode
    totalHours = 0
    if form.weeklyHours != None:
        prefillhours = form.weeklyHours
        allTermForms = LaborStatusForm.select().join_from(LaborStatusForm, Student).where((LaborStatusForm.termCode == form.termCode) & (LaborStatusForm.laborStatusFormID != laborStatusKey) & (LaborStatusForm.studentSupervisee.ID == form.studentSupervisee.ID))
        if allTermForms:
            for i in allTermForms:
                totalHours += i.weeklyHours
    else:
        prefillhours = form.contractHours
    prefillnotes = form.supervisorNotes

    #These are the data fields to populate our dropdowns(Supervisor. Position)
    supervisors = Tracy().getSupervisors()
    positions = Tracy().getPositionsFromDepartment(prefilldepartment)

    #Step 3: send data to front to populate html
    oldSupervisor = Tracy().getSupervisorFromPIDM(form.supervisor.PIDM)

    return render_template( 'main/modifyLSF.html',
				            title=('modify LSF'),
                            username = current_user,
                            superviser_id = superviser_id,
                            prefillstudent = prefillstudent,
                            prefillsupervisor = prefillsupervisor,
                            prefillsupervisorID = prefillsupervisorID,
                            prefilldepartment = prefilldepartment,
                            prefillposition = prefillposition,
                            prefilljobtype = prefilljobtype,
                            prefillterm = prefillterm,
                            prefillhours = prefillhours,
                            prefillnotes = prefillnotes,
                            supervisors = supervisors,
                            positions = positions,
                            form = form,
                            oldSupervisor = oldSupervisor,
                            totalHours = totalHours,
                            currentUser = current_user
                          )

@main_bp.route("/modifyLSF/updateLSF/<laborStatusKey>", methods=['POST'])
def updateLSF(laborStatusKey):
    """ Create Modified Labor Form and Form History"""
    try:
        current_user = require_login()
        if not current_user:        # Not logged in
            return render_template('errors/403.html')
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        rsp = dict(rsp)
        student = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
        for k in rsp:
            LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
            if k == "supervisor":
                d, created = Supervisor.get_or_create(PIDM = int(rsp[k]['newValue']))
                if not created:
                    LSF.supervisor = d.ID
                LSF.save()
                if created:
                    tracyUser = Tracy().getSupervisorFromPIDM(rsp[k]['newValue'])
                    tracyEmail = tracyUser.EMAIL
                    tracyUsername = tracyEmail.find('@')
                    user = Supervisor.get(Supervisor.PIDM == rsp[k]['newValue'])
                    user.username   = tracyEmail[:tracyUsername]
                    user.FIRST_NAME = tracyUser.FIRST_NAME
                    user.LAST_NAME  = tracyUser.LAST_NAME
                    user.EMAIL      = tracyUser.EMAIL
                    user.CPO        = tracyUser.CPO
                    user.ORG        = tracyUser.ORG
                    user.DEPT_NAME  = tracyUser.DEPT_NAME
                    user.ID         = tracyUser.ID
                    user.save()
                    LSF.supervisor = d.PIDM
                    LSF.save()
            if k == "POSN_TITLE":
                LSF.POSN_TITLE = rsp[k]['newValue']
                LSF.save()
            if k == "supervisorNotes":
                LSF.supervisorNotes = rsp[k]['newValue']
                LSF.save()
            if k == "contractHours":
                LSF.contractHours = int(rsp[k]['newValue'])
                LSF.save()
            if k == "weeklyHours":
                allTermForms = LaborStatusForm.select().join_from(LaborStatusForm, Student).where((LaborStatusForm.termCode == LSF.termCode) & (LaborStatusForm.laborStatusFormID != LSF.laborStatusFormID) & (LaborStatusForm.studentSupervisee.ID == LSF.studentSupervisee.ID))
                totalHours = 0
                if allTermForms:
                    for i in allTermForms:
                        totalHours += i.weeklyHours
                previousTotalHours = totalHours + int(rsp[k]['oldValue'])
                newTotalHours = totalHours + int(rsp[k]['newValue'])
                if previousTotalHours <= 15 and newTotalHours > 15:
                    newLaborOverloadForm = OverloadForm.create(studentOverloadReason = "None")
                    newFormHistory = FormHistory.create( formID = laborStatusKey,
                                                        historyType = "Labor Overload Form",
                                                        createdBy = current_user,
                                                        overloadForm = newLaborOverloadForm.overloadFormID,
                                                        createdDate = date.today(),
                                                        status = "Pending")

                    try:
                        overloadEmail = emailHandler(newFormHistory.formHistoryID)
                        overloadEmail.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(newFormHistory.formHistoryID))
                    except Exception as e:
                        print("Error on sending overload emails: ", e)
                elif previousTotalHours > 15 and newTotalHours <= 15:   # This will delete an overload form after the hours are modified
                    deleteOverloadForm = FormHistory.get((FormHistory.formID == laborStatusKey) & (FormHistory.historyType == "Labor Overload Form"))
                    deleteOverloadForm = OverloadForm.get(OverloadForm.overloadFormID == deleteOverloadForm.overloadForm.overloadFormID)
                    deleteOverloadForm.delete_instance()

                LSF.weeklyHours = int(rsp[k]['newValue'])
                LSF.save()
        changedForm = FormHistory.get(FormHistory.formID == laborStatusKey)
        try:
            email = emailHandler(changedForm.formHistoryID)
            email.laborStatusFormModified()
        except Exception as e:
            print("Error on sending form modified emails: ", e)
        message = "Your Labor Status Form for {0} {1} has been modified.".format(student.studentSupervisee.FIRST_NAME, student.studentSupervisee.LAST_NAME)
        flash(message, "success")

        return jsonify({"Success":True})

    except Exception as e:
        message = "An error occured. Your Labor Status Form for {0} {1} was not modified.".format(student.studentSupervisee.FIRST_NAME, student.studentSupervisee.LAST_NAME)
        flash(message, "danger")
        print(e)
        return jsonify({"Success": False})
