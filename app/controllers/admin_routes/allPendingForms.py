#from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
#from flask_login import current_user, login_required
from flask import flash, send_file, json, jsonify, redirect, url_for
from app.login_manager import *
from app.controllers.admin_routes import admin
from app.controllers.errors_routes.handlers import *
from app.models.laborReleaseForm import LaborReleaseForm
from app.models.laborStatusForm import LaborStatusForm
from app.models.modifiedForm import ModifiedForm
from app.models.emailTracker import EmailTracker
from app.models.overloadForm import OverloadForm
from app.models.adminNotes import AdminNotes
from app.logic.emailHandler import *
from app.models.formHistory import *
from app.models.term import Term
from app.logic.banner import Banner
from app import cfg
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash
from app.models.Tracy.stuposn import STUPOSN


@admin.route('/admin/pendingForms/<formType>',  methods=['GET'])
def allPendingForms(formType):
    try:
        current_user = require_login()

        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            isLaborAdmin = False
            return render_template('errors/403.html',
                                    isLaborAdmin = isLaborAdmin)
        else:
            isLaborAdmin = True
        formList = None
        historyType = None
        pageTitle = ""
        approvalTarget = ""
        laborStatusFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Labor Status Form')).count()
        modifiedFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Modified Labor Form')).count()
        releaseFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Labor Release Form')).count()
        overloadFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Labor Overload Form')).count()
        if formType == "pendingLabor":
            historyType = "Labor Status Form"
            approvalTarget = "denyLaborStatusFormsModal"
            pageTitle = "Pending Labor Status Forms"

        elif formType == "pendingAdjustment":
            historyType = "Modified Labor Form"
            approvalTarget = "denyModifiedFormsModal"
            pageTitle = "Pending Adjustment Forms"

        elif formType == "pendingOverload":
            historyType = "Labor Overload Form"
            approvalTarget = "denyOverloadFormsModal"
            pageTitle = "Pending Overload Forms"

        elif formType == "pendingRelease":
            historyType = "Labor Release Form"
            approvalTarget = "denyReleaseformSModal"
            pageTitle = "Pending Release Forms"
        formList = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == historyType).order_by(-FormHistory.createdDate).distinct()
        # only if a form is adjusted
        pendingOverloadFormPairs = {}
        # or allForms.modifiedForm.fieldModified == "Weekly Hours":
        for allForms in formList:
            if allForms.historyType.historyTypeName == "Labor Status Form" or (allForms.historyType.historyTypeName == "Modified Labor Form" and allForms.modifiedForm.fieldModified == "Weekly Hours"):
                try:
                    overloadForm = FormHistory.select().where((FormHistory.formID == allForms.formID) & (FormHistory.historyType == "Labor Overload Form") & (FormHistory.status == "Pending")).get()
                    if overloadForm:
                        pendingOverloadFormPairs[allForms.formHistoryID] = overloadForm.formHistoryID
                except DoesNotExist:
                    pass
                except Exception as e:
                    print(e)
            if allForms.modifiedForm: # If a form has been adjusted then we want to retrieve supervisor and position information using the new values stored in modified table
                # We check if there is a pending overload form using the key of the modifed forms
                if allForms.modifiedForm.fieldModified == "Supervisor": # if supervisor field in adjust forms has been modified,
                    newSupervisorID = allForms.modifiedForm.newValue    # use the supervisor pidm in the field modified to find supervisor in User table.
                    newSupervisor = User.get(User.UserID == newSupervisorID)
                    # we are temporarily storing the supervisor name in new value,
                    # because we want to show the supervisor name in the hmtl template.
                    allForms.modifiedForm.newValue = newSupervisor.FIRST_NAME +" "+ newSupervisor.LAST_NAME
                if allForms.modifiedForm.fieldModified == "Position": # if position field has been modified in adjust form then retriev position name.
                    newPositionCode = allForms.modifiedForm.newValue
                    newPosition = STUPOSN.get(STUPOSN.POSN_CODE == newPositionCode)
                    # temporarily storing the position code and wls in new value, and position name in old value
                    # because we want to show these information in the hmtl template.
                    allForms.modifiedForm.newValue = newPosition.POSN_CODE +" (" + newPosition.WLS+")"
                    allForms.modifiedForm.oldValue = newPosition.POSN_TITLE
        users = User.select()
        return render_template( 'admin/allPendingForms.html',
                                title=pageTitle,
                                username=current_user.username,
                                users=users,
                                formList = formList,
                                formType= formType,
                                modalTarget = approvalTarget,
                                isLaborAdmin = isLaborAdmin,
                                overloadFormCounter = overloadFormCounter,
                                laborStatusFormCounter = laborStatusFormCounter,
                                modifiedFormCounter  = modifiedFormCounter,
                                releaseFormCounter = releaseFormCounter,
                                pendingOverloadFormPairs = pendingOverloadFormPairs
                                )
    except Exception as e:
        print(e)
        return render_template('errors/500.html'), 500

@admin.route('/admin/checkedForms', methods=['POST'])
def approved_and_denied_Forms():
    '''
    This function gets the forms that are checked by the user and inserts them into the database
    '''
    try:
        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            approved_details =  modal_approval_and_denial_data(rsp)
            return jsonify(approved_details)
    except Exception as e:
        print(e)
        return jsonify({"Success": False}),500

@admin.route('/admin/updateStatus/<raw_status>', methods=['POST'])
def finalUpdateStatus(raw_status):
    ''' This method changes the status of the pending forms to approved '''
    current_user = require_login()
    if not current_user:                    # Not logged in
        return render_template('errors/403.html')
    if not current_user.isLaborAdmin:       # Not an admin
        return render_template('errors/403.html')

    if raw_status == 'approved':
        new_status = "Approved"
    elif raw_status == 'denied':
        new_status = "Denied"
    else:
        print("Unknown status: ", raw_status)
        return jsonify({"success": False})
    try:
        createdUser = User.get(username = current_user.username)
        rsp = eval(request.data.decode("utf-8"))
        if new_status == 'Denied':
            # Index 1 will always hold the reject reason in the list, so we can
            # set a variable equal to the index value and then slice off the list
            # item before the iteration
            denyReason = rsp[1]
            rsp = rsp[:1]

        for id in rsp:
            history_type_data = FormHistory.get(FormHistory.formHistoryID == int(id))
            history_type = str(history_type_data.historyType)

            labor_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == history_type)
            labor_forms.status = Status.get(Status.statusName == new_status)
            labor_forms.reviewedDate = date.today()
            labor_forms.reviewedBy = createdUser.UserID
            if new_status == 'Denied':
                labor_forms.rejectReason = denyReason
            labor_forms.save()

            if history_type == "Modified Labor Form" and new_status == "Approved":
                # This function is triggered whenever an adjustment form is approved.
                # The following function overrides the original data in lsf with the new data from adjustment form.
                LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == history_type_data.formID) # getting the specific labor status form
                overrideOriginalStatusFormOnAdjustmentFormApproval(history_type_data, LSF)
        return jsonify({"success": True})
    except Exception as e:
        print("Error preparing form for status update:", e)
        return jsonify({"success": False})

    # BANNER
    save_status = True # default true so that we will still save in the Deny case
    if new_status == 'Approved':
        try:
            conn = Banner()
            save_status = conn.insert(labor_forms)

        except Exception as e:
            print("Unable to update BANNER:", e)
            save_status = False

    if save_status:
        labor_forms.save()
        return jsonify({"success": True})
    else:
        print("Unable to update form status.")
        return jsonify({"success": False}), 500


def overrideOriginalStatusFormOnAdjustmentFormApproval(form, LSF):
    """
    This function checks whether an Adjustment Form is approved. If yes, it overrides the information
    in the original Labor Status Form with the new information coming from approved Adjustment Form.

    The only fields that will ever be modified in an adjustment form are: supervisor, position, and hours.
    """
    current_user = require_login()
    if not current_user:        # Not logged in
            return render_template('errors/403.html')
    if form.modifiedForm.fieldModified == "Supervisor":
        d, created = User.get_or_create(PIDM = form.modifiedForm.newValue)
        if not created:
            LSF.supervisor = d.UserID
        LSF.save()
        if created:
            tracyUser = STUSTAFF.get(STUSTAFF.PIDM == form.modifiedForm.newValue)
            tracyEmail = tracyUser.EMAIL
            tracyUsername = tracyEmail.find('@')
            user = User.get(User.PIDM == form.modifiedForm.newValue)
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
    if form.modifiedForm.fieldModified == "POSN_CODE":
        LSF.POSN_CODE = form.modifiedForm.newValue
        position = STUPOSN.get(STUPOSN.POSN_CODE == form.modifiedForm.newValue)
        LSF.POSN_TITLE = position.POSN_TITLE
        LSF.WLS = position.WLS
        LSF.save()
    if form.modifiedForm.fieldModified == "contractHours":
        LSF.contractHours = form.modifiedForm.newValue
        LSF.save()
    if form.modifiedForm.fieldModified == "weeklyHours":
        allTermForms = LaborStatusForm.select().join_from(LaborStatusForm, Student).where((LaborStatusForm.termCode == LSF.termCode) & (LaborStatusForm.laborStatusFormID != LSF.laborStatusFormID) & (LaborStatusForm.studentSupervisee.ID == LSF.studentSupervisee.ID))
        totalHours = 0
        if allTermForms:
            for i in allTermForms:
                totalHours += i.weeklyHours
        previousTotalHours = totalHours + int(form.modifiedForm.newValue)
        newTotalHours = totalHours + int(form.modifiedForm.newValue)
        if previousTotalHours <= 15 and newTotalHours > 15:
            newLaborOverloadForm = OverloadForm.create(studentOverloadReason = None)
            user = User.get(User.username == current_user)
            newFormHistory = FormHistory.create( formID = LSF.laborStatusFormID,
                                                historyType = "Labor Overload Form",
                                                createdBy = user.UserID,
                                                overloadForm = newLaborOverloadForm.overloadFormID,
                                                createdDate = date.today(),
                                                status = "Pending")
         # TODO: emails are commented out for testing purposes
            # overloadEmail = emailHandler(newFormHistory.formHistoryID)
            # overloadEmail.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(newFormHistory.formHistoryID))
        LSF.weeklyHours = int(form.modifiedForm.newValue)
        LSF.save()


#method extracts data from the data base to papulate pending form approvale modal
def modal_approval_and_denial_data(approval_ids):
    ''' This method grabs the data that populated the on approve modal for lsf'''
    id_list = []
    for formHistoryID in approval_ids:
        fhistory_id = LaborStatusForm.select().join(FormHistory).where(FormHistory.formHistoryID == int(formHistoryID)).get()
        student_details = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == fhistory_id)
        student_firstname, student_lastname = student_details.studentSupervisee.FIRST_NAME, student_details.studentSupervisee.LAST_NAME
        student_name = str(student_firstname) + " " + str(student_lastname)
        student_pos = student_details.POSN_TITLE
        supervisor_firstname, supervisor_lastname = student_details.supervisor.FIRST_NAME, student_details.supervisor.LAST_NAME
        supervisor_name = str(supervisor_firstname) +" "+ str(supervisor_lastname)
        student_hours = student_details.weeklyHours
        student_hours_ch = student_details.contractHours
        tempList = []
        tempList.append(student_name)
        tempList.append(student_pos)
        tempList.append(supervisor_name)
        tempList.append(str(student_hours))
        tempList.append(str(student_hours_ch))
        id_list.append(tempList)
    return(id_list)

@admin.route('/admin/getNotes/<formid>', methods=['GET'])
def getNotes(formid):
    '''
    This function retrieves the supervisor and labor department notes.
    '''
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')
        supervisorNotes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formid) # Gets Supervisor note
        notes = AdminNotes.select().where(AdminNotes.formID == formid) # Gets labor department notes from the laborofficenotes table
        notesDict = {}          # Stores the both types of notes
        if supervisorNotes.supervisorNotes: # If there is a supervisor note, store it in notesDict
            notesDict["supervisorNotes"] = supervisorNotes.supervisorNotes
        if len(notes) > 0: # If there are labor office notes, format, and store them in notesDict
            listOfNotes = []
            for i in range(len(notes)):
                formattedDate = notes[len(notes) -  i - 1].date.strftime('%m/%d/%Y')   # formatting date in the database to display MM/DD/YYYY
                listOfNotes.append("<dl class='dl-horizontal text-left'> <b>" + formattedDate + " | <i>" + notes[len(notes) -  i - 1].createdBy.FIRST_NAME[0] + ". " + notes[len(notes) -  i - 1].createdBy.LAST_NAME + "</i> | </b> " + notes[len(notes) -  i - 1].notesContents + "</dl>")
            notesDict["laborDepartmentNotes"] = listOfNotes
        return jsonify(notesDict)     # return as JSON

    except Exception as e:
        print("error", e)
        return jsonify({"Success": False})

@admin.route('/admin/notesInsert/<formId>', methods=['POST'])
def insertNotes(formId):
    '''
    This function inserts the labor office notes into the database
    '''
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')
        rsp = eval(request.data.decode("utf-8"))
        stripresponse = rsp.strip()
        currentDate = datetime.now().strftime("%Y-%m-%d")  # formats the date to match the peewee format for the database

        if stripresponse:
            AdminNotes.create(formID=formId, createdBy=current_user.UserID, date=currentDate, notesContents=stripresponse) # creates a new entry in the laborOfficeNotes table

            return jsonify({"Success": True})

        elif stripresponse=="" or stripresponse==None:
            flash("No changes made to notes.", "danger")
            return jsonify({"Success": False})

    except Exception as e:
        print(e)
        return jsonify({"Success": False}), 500

@admin.route('/admin/overloadModal/<formHistoryID>', methods=['GET'])
def getOverloadModalData(formHistoryID):
    """
    This function will retrieve the data to populate the overload modal.
    """
    try:
        departmentStatusInfo = {}
        historyForm = FormHistory.select().where(FormHistory.formHistoryID == int(formHistoryID))
        try:
            SAASStatus = historyForm[0].overloadForm.SAASApproved.statusName
            SAASLastEmail = EmailTracker.select().limit(1).where((EmailTracker.recipient == 'SAAS') & (EmailTracker.formID == historyForm[0].formID.laborStatusFormID)) .order_by(EmailTracker.date.desc())
            SAASEmailDate = SAASLastEmail[0].date.strftime('%m/%d/%y')
        except (AttributeError, IndexError):
            # We expect to see the AttributeError and IndexError if there is no data,
            # and in those cases we set the variables manually
            SAASStatus = 'None'
            SAASEmailDate = 'No Email Sent'
        try:
            financialAidStatus = historyForm[0].overloadForm.financialAidApproved.statusName
            financialAidLastEmail = EmailTracker.select().limit(1).where((EmailTracker.recipient == 'Financial Aid') & (EmailTracker.formID == historyForm[0].formID.laborStatusFormID)) .order_by(EmailTracker.date.desc())
            financialAidEmailDate = financialAidLastEmail[0].date.strftime('%m/%d/%y')
        except (AttributeError, IndexError):
            financialAidStatus = 'None'
            financialAidEmailDate = 'No Email Sent'
        try:
            currentPendingForm = FormHistory.select().where((FormHistory.formID == historyForm[0].formID) & (FormHistory.status == "Pending")).get()
            if currentPendingForm:
                pendingForm = True
                pendingFormType = currentPendingForm.historyType.historyTypeName
                if pendingFormType == "Modified Labor Form":
                    pendingFormType = "Labor Adjustment Form"
        except (AttributeError, IndexError):
            pendingForm = False
            pendingFormType = False
        departmentStatusInfo.update({
                            'SAASEmail': SAASEmailDate,
                            'SAASStatus': SAASStatus,
                            'financialAidStatus': financialAidStatus,
                            'financialAidLastEmail': financialAidEmailDate
                            })
        noteTotal = AdminNotes.select().where(AdminNotes.formID == historyForm[0].formID.laborStatusFormID).count()
        return render_template('snips/pendingOverloadModal.html',
                                            historyForm = historyForm,
                                            departmentStatusInfo = departmentStatusInfo,
                                            formHistoryID = historyForm[0].formHistoryID,
                                            laborStatusFormID = historyForm[0].formID.laborStatusFormID,
                                            noteTotal = noteTotal,
                                            pendingForm = pendingForm,
                                            pendingFormType = pendingFormType
                                            )
    except Exception as e:
        return render_template('errors/500.html'), 500

@admin.route('/admin/releaseModal/<formHistoryID>', methods=['GET'])
def getReleaseModalData(formHistoryID):
    """
    This function will retrieve the data to populate the release modal.
    """
    try:
        historyForm = FormHistory.select().where(FormHistory.formHistoryID == int(formHistoryID))
        noteTotal = AdminNotes.select().where(AdminNotes.formID == historyForm[0].formID.laborStatusFormID).count()
        return render_template('snips/pendingReleaseModal.html',
                                            historyForm = historyForm,
                                            formHistoryID = historyForm[0].formHistoryID,
                                            laborStatusFormID = historyForm[0].formID.laborStatusFormID,
                                            noteTotal = noteTotal
                                            )
    except Exception as e:
        return render_template('errors/500.html'), 500

@admin.route('/admin/modalFormUpdate', methods=['POST'])
def modalFormUpdate():
    """
    This function will update the overload or release form based on the form
    type and the data from the modal.
    """
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            historyForm = FormHistory.get(FormHistory.formHistoryID == rsp['formHistoryID'])
            email = emailHandler(historyForm.formHistoryID)
            currentDate = datetime.now().strftime("%Y-%m-%d")
            createdUser = User.get(username = current_user.username)
            status = Status.get(Status.statusName == rsp['status'])
            if rsp['formType'] == 'Overload':
                overloadForm = OverloadForm.get(OverloadForm.overloadFormID == historyForm.overloadForm.overloadFormID)
                overloadForm.laborApproved = status.statusName
                overloadForm.laborApprover = createdUser.UserID
                overloadForm.laborReviewDate = currentDate
                overloadForm.save()
                try:
                    pendingForm = FormHistory.select().where((FormHistory.formID == historyForm.formID) & (FormHistory.status == "Pending")).get()
                    if pendingForm.historyType.historyTypeName == "Modified Labor Form":
                        if pendingForm.modifiedForm.fieldModified != "Weekly Hours":
                            pendingForm = FormHistory.select().join(ModifiedForm).where((FormHistory.formID == historyForm.formID) & (FormHistory.status == "Pending") & (FormHistory.modifiedForm.fieldModified == "Weekly Hours")).get()
                    if pendingForm.historyType.historyTypeName == "Labor Status Form" or (pendingForm.historyType.historyTypeName == "Modified Labor Form" and pendingForm.modifiedForm.fieldModified == "Weekly Hours"):
                        pendingForm.status = status.statusName
                        pendingForm.reviewedBy = createdUser.UserID
                        pendingForm.reviewedDate = currentDate
                        if 'denialReason' in rsp.keys():
                            pendingForm.rejectReason = rsp['denialReason']
                            AdminNotes.create(formID = pendingForm.formID.laborStatusFormID,
                                            createdBy = createdUser.UserID,
                                            date = currentDate,
                                            notesContents = rsp['denialReason'])
                        pendingForm.save()

                        if pendingForm.historyType.historyTypeName == "Labor Status Form":
                            email = emailHandler(pendingForm.formHistoryID)
                            if rsp['status'] in ['Approved', 'Approved Reluctantly']:
                                email.laborStatusFormApproved()
                            elif rsp['status'] == 'Denied':
                                email.laborStatusFormRejected()
                except DoesNotExist:
                    pass
                except Exception as e:
                    print(e)
            if 'denialReason' in rsp.keys():
                # We only update the reject reason if one was given on the UI
                historyForm.rejectReason = rsp['denialReason']
                historyForm.save()
                AdminNotes.create(formID = historyForm.formID.laborStatusFormID,
                                createdBy = createdUser.UserID,
                                date = currentDate,
                                notesContents = rsp['denialReason'])
            if 'adminNotes' in rsp.keys():
                # We only add admin notes if there was a note made on the UI
                AdminNotes.create(formID = historyForm.formID.laborStatusFormID,
                                createdBy = createdUser.UserID,
                                date = currentDate,
                                notesContents = rsp['adminNotes'])
            historyForm.status = status.statusName
            historyForm.reviewedBy = createdUser.UserID
            historyForm.reviewedDate = currentDate
            historyForm.save()
            if rsp['formType'] == 'Overload':
                if rsp['status'] in ['Approved', 'Approved Reluctantly']:
                    email.LaborOverLoadFormApproved()
                elif rsp['status'] == 'Denied':
                    email.LaborOverLoadFormRejected()
            elif rsp['formType'] == 'Release':
                if rsp['status'] == 'Approved':
                    email.laborReleaseFormApproved()
                elif rsp['status'] == 'Denied':
                    email.laborReleaseFormRejected()
            return jsonify({"Success": True})
    except Exception as e:
        print("Error Updating Release/Overload Forms:", e)
        return jsonify({"Success": False}),500

@admin.route('/admin/sendVerificationEmail', methods=['POST'])
def sendEmail():
    """
    This method will send an email to either SAAS or Financial Aid
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            historyForm = FormHistory.get(FormHistory.formHistoryID == rsp['formHistoryID'])
            overloadForm = OverloadForm.get(OverloadForm.overloadFormID == historyForm.overloadForm)
            status = Status.get(Status.statusName == 'Pending')
            if rsp['emailRecipient'] == 'SAASEmail':
                recipient = 'SAAS'
                overloadForm.SAASApproved = status.statusName
                overloadForm.save()
            elif rsp['emailRecipient'] == 'financialAidEmail':
                recipient = 'Financial Aid'
                overloadForm.financialAidApproved = status.statusName
                overloadForm.save()
            # Lines 347-349 were left as comments because they require code from PR #89
            link = '/admin/financialAidOverloadApproval/' + str(rsp['formHistoryID'])
            email = emailHandler(historyForm.formHistoryID)
            email.overloadVerification(recipient, link)
            currentDate = datetime.now().strftime('%m/%d/%y')
            newEmailInformation = {'recipient': recipient,
                                    'emailDate': currentDate,
                                    'status': 'Pending'
            }
            return jsonify(newEmailInformation)
    except Exception as e:
        print("Error sending verification email to SASS/Financial Aid:", e)
        return jsonify({"Success": False}),500

@admin.route('/admin/notesCounter', methods=['POST'])
def getNotesCounter():
    """
    This method retrieve the number of notes a labor status form has
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            noteTotal = AdminNotes.select().where(AdminNotes.formID == rsp['laborStatusFormID']).count()
            noteDictionary = {'noteTotal': noteTotal}
            return jsonify(noteDictionary)
    except Exception as e:
        print("Error selecting admin notes:", e)
        return jsonify({"Success": False}),500
