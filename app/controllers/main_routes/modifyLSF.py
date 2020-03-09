from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.user import User
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.Tracy.stuposn import *
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


@main_bp.route('/modifyLSF/<laborStatusKey>', methods=['GET']) #History modal called it laborStatusKey
def modifyLSF(laborStatusKey):
    ''' This function gets all the form's data and populates the front end with it'''
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    if not current_user.isLaborAdmin:       # Not an admin
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
    superviser_id = form.supervisor.UserID
    prefilldepartment = form.department.DEPT_NAME
    prefillposition = form.POSN_TITLE #+ " " +"("+ form.WLS + ")"
    prefilljobtype = form.jobType
    prefillterm = form.termCode.termName
    if form.weeklyHours != None:
        prefillhours = form.weeklyHours
    else:
        prefillhours = form.contractHours
    prefillnotes = form.supervisorNotes
    #These are the data fields to populate our dropdowns(Supervisor. Position, WLS,)
    supervisors = STUSTAFF.select().where(STUSTAFF.DEPT_NAME == prefilldepartment).order_by(STUSTAFF.FIRST_NAME.asc()) # modeled after LaborStatusForm.py
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == prefilldepartment)
    wls = STUPOSN.select(STUPOSN.WLS).distinct()
    #Step 3: send data to front to populate html
    oldSupervisor = STUSTAFF.get(form.supervisor.PIDM)
    allTermForms = LaborStatusForm.select().join_from(LaborStatusForm, Student).where((LaborStatusForm.termCode == form.termCode) & (LaborStatusForm.laborStatusFormID != laborStatusKey) & (LaborStatusForm.studentSupervisee.ID == form.studentSupervisee.ID))
    totalHours = 0
    if allTermForms:
        for i in allTermForms:
            print(i.weeklyHours)
            totalHours += i.weeklyHours
    print(totalHours)

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
                            wls = wls,
                            form = form,
                            oldSupervisor = oldSupervisor,
                            isLaborAdmin = isLaborAdmin,
                            totalHours = totalHours
                          )

@main_bp.route("/modifyLSF/updateLSF/<laborStatusKey>", methods=['POST'])
def updateLSF(laborStatusKey):
    """ Create Modified Labor Form and Form History"""
    try:
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        rsp = dict(rsp)
        print(rsp)
        student = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey).studentSupervisee.ID
        for k in rsp:
            LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
            if k == "supervisor":
                d, created = User.get_or_create(PIDM = int(rsp[k]['newValue']))
                if not created:
                    LSF.supervisor = d.UserID
                LSF.save()
                if created:
                    tracyUser = STUSTAFF.get(STUSTAFF.PIDM == rsp[k]['newValue'])
                    tracyEmail = tracyUser.EMAIL
                    tracyUsername = tracyEmail.find('@')
                    user = User.get(User.PIDM == rsp[k]['newValue'])
                    user.username   = tracyEmail[:tracyUsername]
                    user.FIRST_NAME = tracyUser.FIRST_NAME
                    user.LAST_NAME  = tracyUser.LAST_NAME
                    user.EMAIL      = tracyUser.EMAIL
                    user.CPO        = tracyUser.CPO
                    user.ORG        = tracyUser.ORG
                    user.DEPT_NAME  = tracyUser.DEPT_NAME
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
                    newLaborOverloadForm = OverloadForm.create(overloadReason = "None")
                    user = User.get(User.username == cfg["user"]["debug"])
                    newFormHistory = FormHistory.create( formID = laborStatusKey,
                                                        historyType = "Labor Overload Form",
                                                        createdBy = user.UserID,
                                                        overloadForm = newLaborOverloadForm.overloadFormID,
                                                        createdDate = date.today(),
                                                        status = "Pending")
                    email = emailHandler(newFormHistory.formHistoryID)
                    email.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(newFormHistory.formHistoryID))
                    email.laborStatusFormModified()
                LSF.weeklyHours = int(rsp[k]['newValue'])
                LSF.save()
                print("We saved")
        # print("Right before we save flash", "=============================")
        # flash("Your labor status form has been modified.", "success")
        print("After the flash")
        return jsonify({"Success":True, "url":"/laborHistory/" + student})
    except Exception as e:
        flash("An error occured.", "danger")
        print(e,"ERRROOOORRRRRR")
        return jsonify({"Success": False})
