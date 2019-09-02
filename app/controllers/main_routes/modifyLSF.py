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

@main_bp.route("/modifyLSF/submitModifiedForm/", methods=['POST'])
def sumbitModifiedForm():
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
            for i in range(len(fieldsModified)):
                ModifiedForm.create(fieldModified = fieldsModified[i],
                                    oldValue      =  oldValues[i],
                                    newValue      =  newValues[i],
                                    effectiveDate =  datetime.strptime(effectiveDates[i], "%m/%d/%Y").strftime('%Y-%m-%d')
                                    )
                # FormHistory.create( formID = lsf.laborStatusFormID, ## needs to be fixed
                #                     historyType = historyType.historyTypeName,
                #                     # modifiedFormID = # the id,
                #                     createdBy   = cfg['user']['debug'],
                #                     createdDate = date.today(),
                #                     status      = status.statusName)



        #         wlsIndexStart = data['Position'].find('(')
        #         wlsIndexEnd = data['Position'].find(')')
        #         wls = data['Position'][wlsIndexStart + 1 : wlsIndexEnd]
        #         bnumberIndex = data['Student'].find('B0')
        #         studentBnumber = data['Student'][bnumberIndex:]
        #         d, created = Student.get_or_create(ID = studentBnumber)
        #         student = d.ID
        #         d, created = User.get_or_create(username = data['Supervisor'])
        #         primarySupervisor = d.username
        #         d, created = Department.get_or_create(DEPT_NAME = data['Department'])
        #         department = d.departmentID
        #         d, created = Term.get_or_create(termCode = data['Term'])
        #         term = d.termCode
        #         start = data['Start Date']
        #         startDate = datetime.strptime(start, "%m/%d/%Y").strftime('%Y-%m-%d')
        #         end = data['End Date']
        #         endDate = datetime.strptime(end, "%m/%d/%Y").strftime('%Y-%m-%d')
        #         lsf = LaborStatusForm.create(termCode = term,
        #                                      studentSupervisee = student,
        #                                      supervisor = primarySupervisor,
        #                                      department  = department,
        #                                      jobType = data['Job Type'],
        #                                      WLS = wls,
        #                                      POSN_TITLE = data['Position'],
        #                                      POSN_CODE = data['Position Code'],
        #                                      contractHours = data.get('Contract Hours', None),
        #                                      weeklyHours   = data.get('Hours Per Week', None),
        #                                      startDate = startDate,
        #                                      endDate = endDate,
        #                                      supervisorNotes = data.get('Supervisor Notes', None)
        #                                      )
        #
        #         historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Status Form")
        #         status = Status.get(Status.statusName == "Pending")
        #         formHistroy = FormHistory.create( formID = lsf.laborStatusFormID,
        #                                           historyType = historyType.historyTypeName,
        #                                           createdBy   = cfg['user']['debug'],
        #                                           createdDate = date.today(),
        #                                           status      = status.statusName)
        #     flash("Labor Status Form(s) has been created.", "success")
        return jsonify({"Success": True})
    except Exception as e:
        flash("An error occured.", "danger")
        print(e)
        return jsonify({"Success": False})
@main_bp.route("/saveChanges/<laborStatusFormID>", methods=["POST"]) #Should this be the reroute or should it be in JS?
def saveChanges(laborStatusFormID):
    #Takes dictionary from ajax and dumps to db
    try:
        laborstatusform = laborStatusForm.get(laborStatusForm.laborStatusFormID==laborStatusFormID)
        data = request.form
        laborstatusform.supervisor = (data['supervisor'])
        laborstatusform.POSN_TITLE = (data['position'])
        laborstatusform.WLS = (data['WLS'])
        laborstatusform.jobType = (data['jobType'])
        laborstatusform.weeklyHours = (data['weeklyHours']) #FIXME: not always weekly hours (if secondary/break).
        laborstatusform.laborSupervisorNotes = (data['laborSupervisorNotes'])
        #modifiedForm #Not sure if this will work...
        modifiedform = modifiedForm.get(modifiedForm.modifiedFormID==modifiedFormID)
        modifiedform.fieldModified = (data['fieldModified'])
        modifiedform.oldValue = (data['oldValue'])
        modifiedform.oldValue = (data['newValue'])
        modifiedform.effectiveDate = (data['effectiveDate'])
        #FIXME: I think this well be a separate save since its a separate dictionary for a separate table
        #old value
        #new value
        #date
    except:
        flash("An error has occurred, your changes were NOT saved. Please try again.","error")
        return json.dumps({"error":0})
