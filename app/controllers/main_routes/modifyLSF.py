from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.user import *
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
        print ("WeeklyHours",prefillhours)
    else:
        prefillhours = form.contractHours
        print ("ContractHours",prefillhours)
    prefillnotes = form.supervisorNotes
    #These are the data fields to populate our dropdowns(Supervisor. Position, WLS,)
    supervisors = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # modeled after LaborStatusForm.py
    positions = STUPOSN.select(STUPOSN.POSN_CODE).distinct()
    wls = STUPOSN.select(STUPOSN.WLS).distinct()
    #Step 3: send data to front to populate html
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
                            form = form
                          )
@main_bp.route("/modifyLSF/getPosition/<department>", methods=['GET'])
def getPosition(department):
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == department)
    position_dict = {}
    for position in positions:
        position_dict[position.POSN_TITLE] = {"position": position.POSN_TITLE, "WLS":position.WLS}
    return json.dumps(position_dict)

@main_bp.route("/modifyLSF/submitModifiedForm/<laborStatusKey>", methods=['POST'])
def sumbitModifiedForm(laborStatusKey):
    """ Create Modified Labor Form and Form History"""
    try:
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        print(rsp)
        if rsp:
            print("Im not empty")
            fieldsModified = list(rsp.keys())
            print(fieldsModified)
            oldValues = []
            newValues  = []
            effectiveDates = []
            for value in fieldsModified:
                newValues.append(rsp[value]["newValue"])
                oldValues.append(rsp[value]["oldValue"])
                effectiveDates.append(rsp[value]["date"])
            print(oldValues)
            print(newValues)
            print(effectiveDates)
            historyType = HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form")
            status = Status.get(Status.statusName == "Pending")
            username = cfg['user']['debug']
            createdbyid = User.get(User.username == username)
            for i in range(len(fieldsModified)):
                #if fieldsModified[i] == "supervisor":
                    #newsupervisor = User.get(User.PIDM == newValues[i])
                    #newValues[i] = newsupervisor.FIRST_NAME + " " + newsupervisor.LAST_NAME

                modifiedforms = ModifiedForm.create(fieldModified = fieldsModified[i],
                                    oldValue      =  oldValues[i],
                                    newValue      =  newValues[i],
                                    effectiveDate =  datetime.strptime(effectiveDates[i], "%m/%d/%Y").strftime('%Y-%m-%d')
                                    )
                formhistorys = FormHistory.create( formID = laborStatusKey,
                                    historyType = historyType.historyTypeName,
                                    # modifiedFormID = # the id
                                    modifiedForm = modifiedforms.modifiedFormID,
                                    createdBy   = createdbyid.UserID,
                                    createdDate = date.today(),
                                    status      = status.statusName)
                for form in range(len(fieldsModified)):
                    try:
                        print(range(len(fieldsModified)))
                        column = str(fieldsModified[form])
                        LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
                        if column == "supervisor":
                            print("i'm here")
                            print(newValues[form])
                            print(LSF.supervisor.UserID)
                            #LSF.supervisor.UserID = newValues[form]
                            #LSF.save()
                            LSF.update_or_create(supervisor.UserID = newValues[form])
                            print(LSF.supervisor.UserID)
                        else:
                            setattr(LSF, column, newValues[form])
                        print("new value form:", newValues[form])
                    except Exception as e:
                        print("I am error")
                        print(e)
        #     flash("Labor Status Form(s) has been created.", "success")
        return jsonify({"Success": True})
    except Exception as e:
        flash("An error occured.", "danger")
        print(e)
        return jsonify({"Success": False})
# @main_bp.route("/saveChanges/<laborStatusFormID>", methods=["POST"]) #Should this be the reroute or should it be in JS?
# def saveChanges(laborStatusFormID):
#     #Takes dictionary from ajax and dumps to db
#     try:
#         laborstatusform = laborStatusForm.get(laborStatusForm.laborStatusFormID==laborStatusFormID)
#         data = request.form
#         laborstatusform.supervisor = (data['supervisor'])
#         laborstatusform.POSN_TITLE = (data['position'])
#         laborstatusform.WLS = (data['WLS'])
#         laborstatusform.jobType = (data['jobType'])
#         laborstatusform.weeklyHours = (data['weeklyHours']) #FIXME: not always weekly hours (if secondary/break).
#         laborstatusform.laborSupervisorNotes = (data['laborSupervisorNotes'])
#         #modifiedForm #Not sure if this will work...
#         modifiedform = modifiedForm.get(modifiedForm.modifiedFormID==modifiedFormID)
#         modifiedform.fieldModified = (data['fieldModified'])
#         modifiedform.oldValue = (data['oldValue'])
#         modifiedform.oldValue = (data['newValue'])
#         modifiedform.effectiveDate = (data['effectiveDate'])
#         #FIXME: I think this well be a separate save since its a separate dictionary for a separate table
#         #old value
#         #new value
#         #date
#     except:
#         flash("An error has occurred, your changes were NOT saved. Please try again.","error")
#         return json.dumps({"error":0})
