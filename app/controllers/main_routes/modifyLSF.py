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
from datetime import *
from flask import json, jsonify
from flask import request
from flask import flash
import base64


@main_bp.route('/modifyLSF/<laborStatusKey>', methods=['GET']) #History modal called it laborStatusKey
def modifyLSF(laborStatusKey):
    ''' This function gets all the form's data and populates the front end with it'''
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)
    form = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
    #Step 2: get prefill data from said form, then the data that populates dropdowns for supervisors and position
    prefillstudent = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME+" ("+form.studentSupervisee.ID+")"
    prefillsupervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
    superviser_id = form.supervisor.UserID
    prefilldepartment = form.department.DEPT_NAME
    prefillposition = form.POSN_TITLE + " " +"("+ form.WLS + ")"
    prefilljobtype = form.jobType
    prefillterm = form.termCode.termName
    if form.weeklyHours != None:
        prefillhours = form.weeklyHours
    else:
        prefillhours = form.contractHours
    prefillnotes = form.supervisorNotes
    #These are the data fields to populate our dropdowns(Supervisor. Position, WLS,)
    supervisors = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # modeled after LaborStatusForm.py
    positions = STUPOSN.select(STUPOSN.POSN_CODE).distinct()
    wls = STUPOSN.select(STUPOSN.WLS).distinct()
    #Step 3: send data to front to populate html
    oldSupervisor = STUSTAFF.get(form.supervisor.PIDM)
    return render_template( 'main/modifyLSF.html',
				            title=('Modify LSF'),
                            username = current_user,
                            superviser_id = superviser_id,
                            prefillstudent = prefillstudent,
                            prefillsupervisor = prefillsupervisor,
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
                            oldSupervisor = oldSupervisor
                          )

@main_bp.route("/modifyLSF/getPosition/<department>", methods=['GET'])
def getPosition(department):
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    supervisors = STUSTAFF.select().where(STUSTAFF.DEPT_NAME == department)
    position_dict = {}
    for supervisor in supervisors:
        position_dict[str(supervisor.PIDM)] = {"supervisorFirstName":supervisor.FIRST_NAME, "supervisorLastName":supervisor.LAST_NAME, "supervisorPIDM":supervisor.PIDM}
    for position in positions:
        position_dict[position.POSN_CODE] = {"position": position.POSN_TITLE, "WLS":position.WLS}
    return json.dumps(position_dict)

@main_bp.route("/modifyLSF/submitModifiedForm/<laborStatusKey>", methods=['POST'])
def sumbitModifiedForm(laborStatusKey):
    """ Create Modified Labor Form and Form History"""
    try:
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        rsp = dict(rsp)
        student = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey).studentSupervisee.ID
        for k in rsp:
            modifiedforms = ModifiedForm.create(fieldModified = k,
                                            oldValue      =  rsp[k]['oldValue'],
                                            newValue      =  rsp[k]['newValue'],
                                            effectiveDate =  datetime.strptime(rsp[k]['date'], "%m/%d/%Y").strftime('%Y-%m-%d')
                                            )
            historyType = HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form")
            status = Status.get(Status.statusName == "Pending")
            username = cfg['user']['debug']
            createdbyid = User.get(User.username == username)
            formhistorys = FormHistory.create( formID = laborStatusKey,
                                             historyType = historyType.historyTypeName,
                                             modifiedForm = modifiedforms.modifiedFormID,
                                             createdBy   = createdbyid.UserID,
                                             createdDate = date.today(),
                                             status      = status.statusName)
            LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
            if k == "supervisor":
                d, created = User.get_or_create(PIDM = rsp[k]['newValue'])
                if not created:
                    LSF.supervisor = d.PIDM
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
                LSF.contractHours = rsp[k]['newValue']
                LSF.save()
            if k == "weeklyHours":
                LSF.weeklyHours = rsp[k]['newValue']
                LSF.save()
            if k == "jobType":
                LSF.jobType = rsp[k]['newValue']
                LSF.save()
        flash("Your labor status form has been modified.", "success")
        return jsonify({"Success":True, "url":"/laborHistory/" + student})
    except Exception as e:
        flash("An error occured.", "danger")
        # print(e)
        return jsonify({"Success": False})
