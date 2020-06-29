from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.formHistory import FormHistory
from app.models.adminNotes import AdminNotes
from app.models.user import User
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.Tracy.stuposn import *
from app.models.modifiedForm import *
from app import cfg
from app.logic.emailHandler import *
from app.login_manager import require_login
from flask_bootstrap import bootstrap_find_resource
from datetime import *
from flask import json, jsonify
from flask import request
from flask import flash
import base64


@main_bp.route("/alterLSF/<laborStatusKey>", methods=["GET"]) #History modal called it laborStatusKey
def alterLSF(laborStatusKey):
    """
    This function gets all the form's data and populates the front end with it
    """
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template("errors/403.html")
    if not current_user.isLaborAdmin:       # Not an admin
        isLaborAdmin = False
    else:
        isLaborAdmin = True
    currentDate = date.today()
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)
    form = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
    # If todays date is greater than the adjustment cut off date on the term and the form is an adjustment LSF,
    # then we do not want to give users access to the adjustment page

    # Query the status of the form to determine if modify or adjust LSF
    formStatus = (FormHistory.select(FormHistory, LaborStatusForm)
                             .join(LaborStatusForm)
                             .where(FormHistory.formID == laborStatusKey)
                             .get().status_id)

    if currentDate > form.termCode.adjustmentCutOff and formStatus == "Approved":
        return render_template("errors/403.html")
    #Step 2: get prefill data from said form, then the data that populates dropdowns for supervisors and position
    prefillstudent = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME+" ("+form.studentSupervisee.ID+")"
    prefillsupervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
    prefillsupervisorID = form.supervisor.PIDM
    superviser_id = form.supervisor.UserID
    prefilldepartment = form.department.DEPT_NAME
    prefillposition = form.POSN_CODE #+ " " +"("+ form.WLS + ")"
    prefilljobtype = form.jobType
    prefillterm = form.termCode.termName
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

    return render_template( "main/alterLSF.html",
				            title=("Adjust Labor Status Form" if formStatus == "Approved" else "Modify Labor Status Form"),
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


@main_bp.route("/alterLSF/submitAlteredLSF/<laborStatusKey>", methods=["POST"])
def submitAlteredLSF(laborStatusKey):
    """
    Submits an altered LSF form and creates a formHistory entry if appropriate
    """
    try:
        current_user = require_login()
        if not current_user:        # Not logged in
            return render_template("errors/403.html")
        currentDate = datetime.now().strftime("%Y-%m-%d")
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        rsp = dict(rsp)
        student = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
        formStatus = (FormHistory.select(FormHistory, LaborStatusForm)
                                 .join(LaborStatusForm)
                                 .where(FormHistory.formID == laborStatusKey)
                                 .get().status_id)

        formHistories = ""
        for k in rsp:
            LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
            if k == "supervisorNotes":
                if formStatus == "Pending":
                    LSF.supervisorNotes = rsp[k]['newValue']
                    LSF.save()
                elif formStatus == "Approved":
                    ## New Entry in AdminNote Table
                    newNoteEntry = AdminNotes.create(formID=LSF.laborStatusFormID,
                                                    createdBy=current_user.UserID,
                                                    date=currentDate,
                                                    notesContents=rsp[k]["newValue"])
                    newNoteEntry.save()
                    continue

            if k == "supervisor":
                if formStatus == "Pending":
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
                        user.ID         = tracyUser.ID
                        user.save()
                        LSF.supervisor = d.PIDM
                        LSF.save()
                elif formStatus == "Approved":
                    formHistories = createFormHistory(laborStatusKey, rsp, k, current_user)

            if k == "position":
                if formStatus == "Pending":
                    LSF.POSN_TITLE = rsp[k]['newValue']
                    LSF.save()
                elif formStatus == "Approved":
                    formHistories = createFormHistory(laborStatusKey, rsp, k, current_user)
            if k == "contractHours":
                if formStatus == "Pending":
                    LSF.contractHours = int(rsp[k]['newValue'])
                    LSF.save()
                elif formStatus == "Approved":
                    formHistories = createFormHistory(laborStatusKey, rsp, k, current_user)
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
                    newFormHistory = FormHistory.create(formID = laborStatusKey,
                                                        historyType = "Labor Overload Form",
                                                        createdBy = current_user.UserID,
                                                        overloadForm = newLaborOverloadForm.overloadFormID,
                                                        createdDate = date.today(),
                                                        status = "Pending")
                    try:
                        if formStatus == "Pending":
                            overloadEmail = emailHandler(newFormHistory.formHistoryID)
                        elif formStatus == "Approved":
                            overloadEmail = emailHandler(formHistories.formHistoryID)
                        overloadEmail.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(newFormHistory.formHistoryID))
                    except Exception as e:
                        print("An error occured while attempting to send overload form emails: ", e)
                if formStatus == "Pending":
                    LSF.weeklyHours = int(rsp[k]['newValue'])
                    LSF.save()
        changedForm = FormHistory.get(FormHistory.formID == laborStatusKey)
        try:
            email = emailHandler(changedForm.formHistoryID)
            email.laborStatusFormModified()
        except Exception as e:
            print("An error occured while attempting to send adjustment form emails: ", e)
        message = "Your Labor Form(s) for {0} {1} has been submitted.".format(student.studentSupervisee.FIRST_NAME, student.studentSupervisee.LAST_NAME)
        flash(message, "success")

        if formStatus == "Pending":
            return jsonify({"Success": True})
        elif formStatus == "Approved":
            return jsonify({"Success": True, "url":"/laborHistory/" + student.studentSupervisee.ID})

    except Exception as e:
        message = "An error occured. Your labor {0} form(s) for {1} {2} were not submitted.".format("status" if formStatus == "Pending" else "adjustment",
                                                                                                    student.studentSupervisee.FIRST_NAME,
                                                                                                    student.studentSupervisee.LAST_NAME)
        flash(message, "danger")
        print("An error occured during form submission:", e)
        return jsonify({"Success": False})

def createFormHistory(laborStatusKey, rsp, k, current_user):
    """
    Creates appropriate form history entries in the formHistory table
    """
    modifiedforms = ModifiedForm.create(fieldModified = k,
                                        oldValue      = rsp[k]['oldValue'],
                                        newValue      = rsp[k]['newValue'],
                                        effectiveDate = datetime.strptime(rsp[k]['date'], "%m/%d/%Y").strftime('%Y-%m-%d')
                                        )
    historyType = HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form")
    status = Status.get(Status.statusName == "Pending")
    formHistories = FormHistory.create(formID = laborStatusKey,
                                     historyType = historyType.historyTypeName,
                                     modifiedForm = modifiedforms.modifiedFormID,
                                     createdBy   = current_user.UserID,
                                     createdDate = date.today(),
                                     status      = status.statusName)
    return formHistories
