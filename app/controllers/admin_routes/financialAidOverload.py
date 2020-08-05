from app.controllers.admin_routes import admin
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *
from flask import json, jsonify
from flask import request, render_template, flash
from app.models.overloadForm import *
from app import cfg
from app.models.adminNotes import AdminNotes
from datetime import datetime, date
from app.models.status import *
from app.logic.emailHandler import*

@admin.route('/admin/financialAidOverloadApproval/<overloadKey>', methods=['GET']) # we get the form ID when FinancialAid or SAAS clicks on the link they receive via email.
def financialAidOverload(overloadKey):
    '''
    This function prefills all the information for a student's current job and overload request.
    '''
    currentUser = require_login() #we need to check to see if the person logged in is SAAS or FinancialAid

    if not currentUser: # Not logged in
        return render_template('errors/403.html'), 403
    if not (currentUser.isFinancialAidAdmin or currentUser.isSaasAdmin): # Not an admin
        return render_template('errors/403.html'), 403

    overloadForm = FormHistory.get(FormHistory.formHistoryID == overloadKey) # get access to overload form
    lsfForm = overloadForm.formID #LaborStatusForm.get(LaborStatusForm.laborStatusFormID == overloadForm.formID) # get the labor status form that is tied to the overload form


    overloadForm = FormHistory.get(FormHistory.overloadForm == overloadKey) # get access to overload form
    lsfForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == overloadForm.formID) # get the labor status form that is tied to the overload form

    totalHours = {}
    ###-------- Popoulate Current Position -------###
    # Get all labor status forms for the same student in the same term and see if they have a primary position.
    # IF YES: populate the "Current Position" Fields with the information from that labor status form.
    allLaborStatusForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == lsfForm.studentSupervisee.ID, LaborStatusForm.termCode == lsfForm.termCode.termCode)
    statusList = ["Approved", "Approved Reluctantly", "Pending"]
    for form in allLaborStatusForms:
        studentHistory = FormHistory.get(FormHistory.formID == form.laborStatusFormID) # prepopulate only and only if primary labor status form is not denied
        if form.jobType == "Primary":
            if studentHistory.status.statusName in statusList:
                studentName = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME
                studentBnum = form.studentSupervisee.ID
                position = form.POSN_TITLE
                supervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
                department = form.department.DEPT_NAME
                primaryPositionHours = form.weeklyHours
                totalHours["primaryHours"] = primaryPositionHours
                totalHours["secondaryHours"] = 0
        if form.jobType == "Secondary" and studentHistory.historyType.historyTypeName == "Labor Status Form":
            totalHours["secondaryHours"] = form.weeklyHours

    ###-------- Popoulate Overload Request Information -------###
    # Get the overload form submitted for the student. Then, populate the Overload Request Information section with the data from overload form.
    overloadPosition = lsfForm.POSN_TITLE
    totalOverloadHours = lsfForm.weeklyHours + totalHours["primaryHours"] + totalHours["secondaryHours"]
    studentOverloadReason = overloadForm.overloadForm.studentOverloadReason
    laborOfficeNotes = lsfForm.laborDepartmentNotes
    contractDate = "{} - {}".format(lsfForm.startDate.strftime('%m/%d/%Y'), lsfForm.endDate.strftime('%m/%d/%Y'))

# will need to add term to the interface and then have a prefill variable
    return render_template( 'admin/financialAidOverload.html',
                        username = currentUser,
                        overload = overloadForm,
                        studentName = studentName,
                        studentBnum = studentBnum,
                        department = department,
                        position = position,
                        supervisor= supervisor,
                        primaryPositionHours = primaryPositionHours,
                        studentOverloadReason = studentOverloadReason,
                        laborOfficeNotes = laborOfficeNotes,
                        contractDate = contractDate,
                        overloadPosition = overloadPosition,
                        totalOverloadHours = totalOverloadHours
                      )

@admin.route("/admin/financialAidOverloadApproval/<status>", methods=["POST"])
def formDenial(status):
    ''' This fucntion will get the status (Approved/Denied) and make the appropriate
    changes in the database for that specific overload form'''
    try:
        currentUser = require_login() #we need to check to see if the person logged in is SAAS or FinancialAid
        if not currentUser: # Not logged in
            return render_template('errors/403.html'), 403
        if not (currentUser.isFinancialAidAdmin or currentUser.isSaasAdmin): # Not an admin
            return render_template('errors/403.html'), 403
        if status == "denied":
            newStatus = "Denied"
        elif status == "approved":
            newStatus = "Approved"
        else:
            return jsonify({'error': 'Unknown Status'}), 500

        rsp = eval(request.data.decode("utf-8"))
        currentDate = datetime.now().strftime("%Y-%m-%d")
        selectedFormHistory = FormHistory.get(FormHistory.formHistoryID == rsp["formHistoryID"])
        selectedOverload = OverloadForm.get(OverloadForm.overloadFormID == selectedFormHistory.overloadForm.overloadFormID)
        formStatus = Status.get(Status.statusName == newStatus)
        if rsp:
            ## New Entry in AdminNote Table
            newNoteEntry = AdminNotes.create(formID=selectedFormHistory.formID.laborStatusFormID,
            createdBy=currentUser, date=currentDate,
            notesContents=rsp["denialNote"])
            newNoteEntry.save()
            ## Updating the overloadform Table
            if currentUser.isFinancialAidAdmin:
                selectedOverload.financialAidApproved = formStatus.statusName
                selectedOverload.financialAidApprover = currentUser
                selectedOverload.financialAidReviewDate = currentDate
                selectedOverload.save()
            if currentUser.isSaasAdmin:
                selectedOverload.SAASApproved = formStatus.statusName
                selectedOverload.SAASApprover = currentUser
                selectedOverload.SAASReviewDate = currentDate
                selectedOverload.save()
        # email = emailHandler(rsp["formHistoryID"]) ## sending email to Labor Admin on any submission
        # email.verifiedOverloadNotification()
        return jsonify({'success':True}), 200
    except Exception as e:
        print("Unable to Deny the OverloadForm",type(e).__name__ + ":", e)
        return jsonify({'error': "Unable to Deny the form"}), 500
