from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.formHistory import FormHistory
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
from datetime import date
from app import cfg
from app.logic.emailHandler import*
from app.models.adminNotes import AdminNotes


@main_bp.route('/adjustLSF/<laborStatusKey>', methods=['GET']) #History modal called it laborStatusKey
def adjustLSF(laborStatusKey):
    ''' This function gets all the form's data and populates the front end with it'''
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    if not current_user.isLaborAdmin:       # Not an admin
        if current_user.Student and not current_user.Supervisor: # If a student is logged in and trying to get to this URL then send them back to their own page.
            return redirect('/laborHistory/' + current_user.Student.ID)
    currentDate = date.today()
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)
    form = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
    # If todays date is greater than the adjustment cut off date on the term, then we do not want to
    # give users access to the adjustment page
    if currentDate > form.termCode.adjustmentCutOff:
        return render_template('errors/403.html')
    #Step 2: get prefill data from said form, then the data that populates dropdowns for supervisors and position
    prefillstudent = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME+" ("+form.studentSupervisee.ID+")"
    prefillsupervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
    prefillsupervisorID = form.supervisor.PIDM
    superviser_id = form.supervisor.ID
    prefilldepartment = form.department.DEPT_NAME
    prefillposition = form.POSN_CODE #+ " " +"("+ form.WLS + ")"
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
    #These are the data fields to populate our dropdowns(Supervisor. Position, WLS,)
    supervisors = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # modeled after LaborStatusForm.py
    positions = STUPOSN.select().where(STUPOSN.DEPT_NAME == prefilldepartment)
    wls = STUPOSN.select(STUPOSN.WLS).distinct()
    #Step 3: send data to front to populate html
    oldSupervisor = STUSTAFF.get(form.supervisor.PIDM)

    return render_template( 'main/adjustLSF.html',
				            title=('adjust LSF'),
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
                            totalHours = totalHours,
                            currentUser = current_user
                          )


@main_bp.route("/adjustLSF/submitModifiedForm/<laborStatusKey>", methods=['POST'])
def sumbitModifiedForm(laborStatusKey):
    """ Create Modified Labor Form and Form History"""
    try:
        current_user = require_login()
        if not current_user:        # Not logged in
            return render_template('errors/403.html')
        currentDate = datetime.now().strftime("%Y-%m-%d")
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        rsp = dict(rsp)
        student = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
        for k in rsp:
            LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
            if k == "supervisorNotes":
                ## New Entry in AdminNote Table
                newNoteEntry = AdminNotes.create(formID=LSF.laborStatusFormID,
                                                createdBy=current_user,
                                                date=currentDate,
                                                notesContents=rsp[k]["newValue"])
                newNoteEntry.save()
            else:
                modifiedforms = ModifiedForm.create(fieldModified = k,
                                                oldValue      =  rsp[k]['oldValue'],
                                                newValue      =  rsp[k]['newValue'],
                                                effectiveDate =  datetime.strptime(rsp[k]['date'], "%m/%d/%Y").strftime('%Y-%m-%d')
                                                )
            historyType = HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form")
            status = Status.get(Status.statusName == "Pending")
            formHistories = FormHistory.create( formID = laborStatusKey,
                                             historyType = historyType.historyTypeName,
                                             modifiedForm = modifiedforms.modifiedFormID,
                                             createdBy   = current_user,
                                             createdDate = date.today(),
                                             status      = status.statusName)

            if k == "Weekly Hours":
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
                        overloadEmail = emailHandler(formHistories.formHistoryID)
                        overloadEmail.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(newFormHistory.formHistoryID))
                    except Exception as e:
                        print("Error on sending overload form emails: ", e)
        try:
            email = emailHandler(formHistories.formHistoryID)
            email.laborStatusFormModified()
        except Exception as e:
            print("Error on sending adjustment form emails: ", e)
        message = "Your Labor Adjustment Form(s) for {0} {1} has been submitted.".format(student.studentSupervisee.FIRST_NAME, student.studentSupervisee.LAST_NAME)
        flash(message, "success")

        return jsonify({"Success":True, "url":"/laborHistory/" + student.studentSupervisee.ID})
    except Exception as e:
        message = "An error occured. Your Labor Adjustment Form(s) for {0} {1} was not submitted.".format(student.studentSupervisee.FIRST_NAME, student.studentSupervisee.LAST_NAME)
        flash(message, "danger")
        print("Error Occured On Adjustment Form Submission:", e)
        return jsonify({"Success": False})
