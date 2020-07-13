from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.formHistory import FormHistory
from app.models.user import User
from app.models.adjustedForm import AdjustedForm
from app import cfg
from app.logic.emailHandler import *
from app.login_manager import require_login
from app.logic.tracy import Tracy
from app.models.adminNotes import AdminNotes
from app.models.supervisor import Supervisor
from app.login_manager import require_login
from datetime import date, datetime
from flask import json, jsonify
from flask import request
from flask import flash
import base64


@main_bp.route("/alterLSF/<laborStatusKey>", methods=["GET"])
def alterLSF(laborStatusKey):
    """
    This function gets all the form's data and populates the front end
    """
    currentUser = require_login()
    if not currentUser:        # Not logged in
        return render_template("errors/403.html")
    if not currentUser.isLaborAdmin:       # Not an admin
        if currentUser.Student and not currentUser.Supervisor: # If a student is logged in and trying to get to this URL then send them back to their own page.
            return redirect("/laborHistory/" + currentUser.Student.ID)

    currentDate = date.today()
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)
    form = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
    # If todays date is greater than the adjustment cut off date on the term and the form is an adjustment LSF,
    # then we do not want to give users access to the adjustment page

    # Query the status of the form to determine if correction or adjust LSF
    formStatus = (FormHistory.select(FormHistory, LaborStatusForm)
                             .join(LaborStatusForm)
                             .where(FormHistory.formID == laborStatusKey)
                             .get().status_id)

    if currentDate > form.termCode.adjustmentCutOff and formStatus == "Approved":
        return render_template("errors/403.html", currentUser = currentUser)
    #Step 2: get prefill data from said form, then the data that populates dropdowns for supervisors and position
    prefillstudent = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME+" ("+form.studentSupervisee.ID+")"
    prefillsupervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
    prefillsupervisorID = form.supervisor.ID
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

    #These are the data fields to populate our dropdowns(Supervisor. Position)
    supervisors = Tracy().getSupervisors()
    positions = Tracy().getPositionsFromDepartment(prefilldepartment)

    #Step 3: send data to front to populate html
    oldSupervisor = Tracy().getSupervisorFromID(form.supervisor.ID)

    return render_template( "main/alterLSF.html",
				            title=("Adjust Labor Status Form" if formStatus == "Approved" else "Labor Status Correction Form"),
                            username = currentUser,
                            superviser_id = superviser_id,
                            prefillstudent = prefillstudent,
                            prefillsupervisor = prefillsupervisor,
                            prefillsupervisorPIDM = prefillsupervisorPIDM,
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
                            currentUser = currentUser
                          )


@main_bp.route("/alterLSF/submitAlteredLSF/<laborStatusKey>", methods=["POST"])
def submitAlteredLSF(laborStatusKey):
    """
    Submits an altered LSF form and creates a formHistory entry if appropriate
    """
    try:
        currentUser = require_login()
        if not currentUser:        # Not logged in
            return render_template("errors/403.html")
        currentDate = datetime.now().strftime("%Y-%m-%d")
        rsp = eval(request.data.decode("utf-8")) # This fixes byte indices must be intergers or slices error
        rsp = dict(rsp)
        student = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
        # formStatus = (FormHistory.select(FormHistory, LaborStatusForm)
        #                          .join(LaborStatusForm)
        #                          .where(FormHistory.formID == laborStatusKey)
        #                          .get().status_id)
        formStatus = (FormHistory.get(FormHistory.formID == laborStatusKey).status_id)
        formHistories = ""
        for k in rsp:
            LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
            if k == "supervisorNotes":
                if formStatus == "Pending":
                    LSF.supervisorNotes = rsp[k]['newValue']
                    LSF.save()
                elif formStatus == "Approved":
                    ## New Entry in AdminNote Table
                    newNoteEntry = AdminNotes.create(formID        = LSF.laborStatusFormID,
                                                     createdBy     = currentUser,
                                                     date          = currentDate,
                                                     notesContents = rsp[k]["newValue"])
                    newNoteEntry.save()
                    continue
            # This creates the adjusted form entry for every changed field for an adjustment submission
            elif formStatus == "Approved":
                adjustedforms = AdjustedForm.create(fieldAdjusted = k,
                                                    oldValue      = rsp[k]['oldValue'],
                                                    newValue      = rsp[k]['newValue'],
                                                    effectiveDate = datetime.strptime(rsp[k]['date'], "%m/%d/%Y").strftime('%Y-%m-%d'))
                historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Adjustment Form")
                status = Status.get(Status.statusName == "Pending")
                formHistories = FormHistory.create(formID       = laborStatusKey,
                                                   historyType  = historyType.historyTypeName,
                                                   adjustedForm = adjustedforms.adjustedFormID,
                                                   createdBy    = currentUser,
                                                   createdDate  = date.today(),
                                                   status       = status.statusName)

            if k == "supervisor":
                if formStatus == "Pending":
                    # d, created = User.get_or_create(Supervisor = rsp[k]['newValue'])
                    d, created = Supervisor.get_or_create(ID = rsp[k]['newValue'])
                    if not created:
                        LSF.supervisor = d.ID
                    LSF.save()
                    if created:
                        print("This ran")
                        tracyUser = Tracy().getSupervisorFromID(rsp[k]['newValue'])
                        tracyEmail = tracyUser.EMAIL
                        tracyUsername = tracyEmail.find('@')
                        user = User.get(User.userID == rsp[k]['newValue'])
                        user.username   = tracyEmail[:tracyUsername]
                        user.Supervisor = tracyUser.ID
                        user.save()

                        supervisor = Supervisor.get_or_create(ID = tracyUser.ID)
                        supervisor.FIRST_NAME = tracyUser.LAST_NAME
                        supervisor.LAST_NAME = tracyUser.FIRST_NAME
                        supervisor.EMAIL = tracyUser.EMAIL
                        supervisor.CPO = tracyUser.CPO
                        supervisor.ORG = tracyUser.ORG
                        supervisor.DEPT_NAME = tracyUser.DEPT_NAME
                        supervisor.save()
                        LSF.supervisor = d.ID
                        LSF.save()

            if k == "position":
                if formStatus == "Pending":
                    position = Tracy().getPositionFromCode(rsp[k]['newValue'])
                    LSF.POSN_CODE = position.POSN_CODE
                    LSF.POSN_TITLE = position.POSN_TITLE
                    LSF.WLS = position.WLS
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
                    newFormHistory = FormHistory.create(formID       = laborStatusKey,
                                                        historyType  = "Labor Overload Form",
                                                        createdBy    = currentUser,
                                                        overloadForm = newLaborOverloadForm.overloadFormID,
                                                        createdDate  = date.today(),
                                                        status       = "Pending")
                    try:
                        if formStatus == "Pending":
                            overloadEmail = emailHandler(newFormHistory.formHistoryID)
                        elif formStatus == "Approved":
                            overloadEmail = emailHandler(formHistories.formHistoryID)
                        overloadEmail.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(newFormHistory.formHistoryID))
                    except Exception as e:
                        print("An error occured while attempting to send overload form emails: ", e)
                elif previousTotalHours > 15 and newTotalHours <= 15:   # This will delete an overload form after the hours are changed
                    deleteOverloadForm = FormHistory.get((FormHistory.formID == laborStatusKey) & (FormHistory.historyType == "Labor Overload Form"))
                    deleteOverloadForm = OverloadForm.get(OverloadForm.overloadFormID == deleteOverloadForm.overloadForm.overloadFormID)
                    deleteOverloadForm.delete_instance()
                if formStatus == "Pending":
                    LSF.weeklyHours = int(rsp[k]['newValue'])
                    LSF.save()
        changedForm = FormHistory.get(FormHistory.formID == laborStatusKey)
        try:
            email = emailHandler(changedForm.formHistoryID)
            email.laborStatusFormAdjusted()
        except Exception as e:
            print("An error occured while attempting to send adjustment form emails: ", e)
        message = "Your labor {0} form(s) for {1} {2} have been submitted.".format("adjustment" if formStatus == "Approved" else "modification",
                                                                                   student.studentSupervisee.FIRST_NAME,
                                                                                   student.studentSupervisee.LAST_NAME)
        flash(message, "success")
        return jsonify({"Success": True})

    except Exception as e:
        message = "An error occured. Your labor {0} form(s) for {1} {2} were not submitted.".format("status" if formStatus == "Pending" else "adjustment",
                                                                                                    student.studentSupervisee.FIRST_NAME,
                                                                                                    student.studentSupervisee.LAST_NAME)
        flash(message, "danger")
        print("An error occured during form submission:", e)
        return jsonify({"Success": False}), 500
