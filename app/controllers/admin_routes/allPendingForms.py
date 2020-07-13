#from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
#from flask_login import current_user, login_required
from flask import flash, send_file, json, jsonify, redirect, url_for
from app.login_manager import *
from app.controllers.admin_routes import admin
from app.controllers.errors_routes.handlers import *
from app.models.laborReleaseForm import LaborReleaseForm
from app.models.laborStatusForm import LaborStatusForm
from app.models.adjustedForm import AdjustedForm
from app.models.emailTracker import EmailTracker
from app.models.overloadForm import OverloadForm
from app.models.adminNotes import AdminNotes
from app.logic.emailHandler import *
from app.models.formHistory import *
from app.models.term import Term
from app.logic.banner import Banner
from app.logic.tracy import Tracy
from app import cfg
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash
from app.models.Tracy.stuposn import STUPOSN
from app.models.supervisor import Supervisor


@admin.route('/admin/pendingForms/<formType>',  methods=['GET'])
def allPendingForms(formType):
    try:
        currentUser = require_login()
        if not currentUser:                    # Not logged in
            return render_template('errors/403.html')
        if not currentUser.isLaborAdmin:       # Not an admin
            if currentUser.Student: # logged in as a student
                return redirect('/laborHistory/' + currentUser.Student.ID)
            elif currentUser.Supervisor:
                return render_template('errors/403.html', currentUser = currentUser), 403
        formList = None
        historyType = None
        pageTitle = ""
        approvalTarget = ""
        laborStatusFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Labor Status Form')).count()
        adjustedFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Labor Adjustment Form')).count()
        releaseFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Labor Release Form')).count()
        overloadFormCounter = FormHistory.select().where((FormHistory.status == 'Pending') & (FormHistory.historyType == 'Labor Overload Form')).count()
        if formType == "pendingLabor":
            historyType = "Labor Status Form"
            approvalTarget = "denyLaborStatusFormsModal"
            pageTitle = "Pending Labor Status Forms"

        elif formType == "pendingAdjustment":
            historyType = "Labor Adjustment Form"
            approvalTarget = "denyAdjustedFormsModal"
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
        # or allForms.adjustedForm.fieldAdjusted == "Weekly Hours":
        for allForms in formList:
            if allForms.historyType.historyTypeName == "Labor Status Form" or (allForms.historyType.historyTypeName == "Labor Adjustment Form" and allForms.adjustedForm.fieldAdjusted == "weeklyHours"):
                try:
                    overloadForm = FormHistory.select().where((FormHistory.formID == allForms.formID) & (FormHistory.historyType == "Labor Overload Form") & (FormHistory.status == "Pending")).get()
                    if overloadForm:
                        pendingOverloadFormPairs[allForms.formHistoryID] = overloadForm.formHistoryID
                except DoesNotExist:
                    pass
                except Exception as e:
                    print(e)
            if allForms.adjustedForm: # If a form has been adjusted then we want to retrieve supervisor and position information using the new values stored in adjusted table
                # We check if there is a pending overload form using the key of the modifed forms
                if allForms.adjustedForm.fieldAdjusted == "supervisor": # if supervisor field in adjust forms has been changed,
                    newSupervisorID = allForms.adjustedForm.newValue    # use the supervisor pidm in the field adjusted to find supervisor in User table.
                    newSupervisor = Supervisor.get(Supervisor.ID == newSupervisorID)
                    # we are temporarily storing the supervisor name in new value,
                    # because we want to show the supervisor name in the hmtl template.
                    allForms.adjustedForm.newValue = newSupervisor.FIRST_NAME +" "+ newSupervisor.LAST_NAME

                if allForms.adjustedForm.fieldAdjusted == "position": # if position field has been changed in adjust form then retriev position name.
                    newPositionCode = allForms.adjustedForm.newValue
                    newPosition = Tracy().getPositionFromCode(newPositionCode)
                    # temporarily storing the position code and wls in new value, and position name in old value
                    # because we want to show these information in the hmtl template.
                    allForms.adjustedForm.newValue = newPosition.POSN_CODE +" (" + newPosition.WLS+")"
                    allForms.adjustedForm.oldValue = newPosition.POSN_TITLE
        users = Supervisor.select()
        return render_template( 'admin/allPendingForms.html',
                                title=pageTitle,
                                username=currentUser.username,
                                users=users,
                                formList = formList,
                                formType= formType,
                                modalTarget = approvalTarget,
                                overloadFormCounter = overloadFormCounter,
                                laborStatusFormCounter = laborStatusFormCounter,
                                adjustedFormCounter  = adjustedFormCounter,
                                releaseFormCounter = releaseFormCounter,
                                currentUser = currentUser,
                                pendingOverloadFormPairs = pendingOverloadFormPairs
                                )
    except Exception as e:
        print("Error Loading all Pending Forms:", e)
        return render_template('errors/500.html', currentUser = currentUser), 500

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
    currentUser = require_login()
    if not currentUser:                    # Not logged in
        return render_template('errors/403.html')
    if not currentUser.isLaborAdmin:       # Not an admin
        return render_template('errors/403.html', currentUser = currentUser), 403

    if raw_status == 'approved':
        new_status = "Approved"
    elif raw_status == 'denied':
        new_status = "Denied"
    else:
        print("Unknown status: ", raw_status)
        return jsonify({"success": False})
    try:
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
            labor_forms.reviewedBy = currentUser
            if new_status == 'Denied':
                labor_forms.rejectReason = denyReason
            labor_forms.save()

            if history_type_data.adjustedForm and new_status == "Approved":
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

    The only fields that will ever be changed in an adjustment form are: supervisor, position, and hours.
    """
    currentUser = require_login()
    if not currentUser:        # Not logged in
            return render_template('errors/403.html')
    if form.adjustedForm.fieldAdjusted == "supervisor":
        d, created = Supervisor.get_or_create(ID = form.adjustedForm.newValue)
        if not created:
            LSF.supervisor = d.ID
        LSF.save()
        if created:
            tracyUser = Tracy().getSupervisorFromPIDM(form.adjustedForm.newValue)
            tracyEmail = tracyUser.EMAIL
            tracyUsername = tracyEmail.find('@')
            user = Supervisor.get(Supervisor.ID == form.adjustedForm.newValue)
            user.username   = tracyEmail[:tracyUsername]
            user.FIRST_NAME = tracyUser.FIRST_NAME
            user.LAST_NAME  = tracyUser.LAST_NAME
            user.EMAIL      = tracyUser.EMAIL
            user.CPO        = tracyUser.CPO
            user.ORG        = tracyUser.ORG
            user.DEPT_NAME  = tracyUser.DEPT_NAME
            user.save()
            LSF.supervisor = d.ID
            LSF.save()

    if form.adjustedForm.fieldAdjusted == "position":
        LSF.POSN_CODE = form.adjustedForm.newValue
        position = Tracy().getPositionFromCode(form.adjustedForm.newValue)
        LSF.POSN_TITLE = position.POSN_TITLE
        LSF.WLS = position.WLS
        LSF.save()

    if form.adjustedForm.fieldAdjusted == "contractHours":
        LSF.contractHours = int(form.adjustedForm.newValue)
        LSF.save()

    if form.adjustedForm.fieldAdjusted == "weeklyHours":
        LSF.weeklyHours = int(form.adjustedForm.newValue)
        LSF.save()


#method extracts data from the data base to papulate pending form approvale modal
def modal_approval_and_denial_data(approval_ids):
    ''' This method grabs the data that populated the on approve modal for lsf'''

    id_list = []
    for formHistoryID in approval_ids:
        formHistory = FormHistory.get(FormHistory.formHistoryID == int(formHistoryID))
        fhistory_id = LaborStatusForm.select().join(FormHistory).where(FormHistory.formHistoryID == int(formHistoryID)).get()
        student_details = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == fhistory_id)
        student_firstname, student_lastname = student_details.studentSupervisee.FIRST_NAME, student_details.studentSupervisee.LAST_NAME
        student_name = str(student_firstname) + " " + str(student_lastname)
        student_pos = student_details.POSN_TITLE
        supervisor_firstname, supervisor_lastname = student_details.supervisor.FIRST_NAME, student_details.supervisor.LAST_NAME
        supervisor_name = str(supervisor_firstname) + " " + str(supervisor_lastname)
        student_hours = student_details.weeklyHours
        student_hours_ch = student_details.contractHours

        if formHistory.adjustedForm:
            if formHistory.adjustedForm.fieldAdjusted == "position":
                position = Tracy().getPositionFromCode(formHistory.adjustedForm.newValue)
                student_pos = position.POSN_TITLE
            if formHistory.adjustedForm.fieldAdjusted == "supervisor":
                supervisor = Supervisor.get(Supervisor.ID == formHistory.adjustedForm.newValue)
                supervisor_firstname, supervisor_lastname = supervisor.FIRST_NAME, supervisor.LAST_NAME
                supervisor_name = str(supervisor_firstname) +" "+ str(supervisor_lastname)
            if formHistory.adjustedForm.fieldAdjusted == "weeklyHours":
                student_hours = formHistory.adjustedForm.newValue
            if formHistory.adjustedForm.fieldAdjusted == "contractHours":
                student_hours_ch = formHistory.adjustedForm.newValue

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
        currentUser = require_login()
        if not currentUser:                    # Not logged in
            return render_template('errors/403.html')
        if not currentUser.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html', currentUser = currentUser), 403
        supervisorNotes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formid) # Gets Supervisor note
        notes = AdminNotes.select().where(AdminNotes.formID == formid) # Gets labor department notes from the laborofficenotes table
        notesDict = {}          # Stores the both types of notes
        if supervisorNotes.supervisorNotes: # If there is a supervisor note, store it in notesDict
            notesDict["supervisorNotes"] = supervisorNotes.supervisorNotes
        if len(notes) > 0: # If there are labor office notes, format, and store them in notesDict
            listOfNotes = []
            for i in range(len(notes)):
                formattedDate = notes[len(notes) -  i - 1].date.strftime('%m/%d/%Y')   # formatting date in the database to display MM/DD/YYYY
                listOfNotes.append("<dl class='dl-horizontal text-left'> <b>" + formattedDate + " | <i>" + notes[len(notes) -  i - 1].createdBy.Supervisor.FIRST_NAME[0] + ". " + notes[len(notes) -  i - 1].createdBy.Supervisor.LAST_NAME + "</i> | </b> " + notes[len(notes) -  i - 1].notesContents + "</dl>")
            notesDict["laborDepartmentNotes"] = listOfNotes
        return jsonify(notesDict)     # return as JSON

    except Exception as e:
        print("Error on getting notes: ", e)
        return jsonify({"Success": False})

@admin.route('/admin/notesInsert/<formId>', methods=['POST'])
def insertNotes(formId):
    '''
    This function inserts the labor office notes into the database
    '''
    try:
        currentUser = require_login()
        if not currentUser:                    # Not logged in
            return render_template('errors/403.html')
        if not currentUser.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html', currentUser = currentUser), 403
        rsp = eval(request.data.decode("utf-8"))
        stripresponse = rsp.strip()
        currentDate = datetime.now().strftime("%Y-%m-%d")  # formats the date to match the peewee format for the database

        if stripresponse:
            AdminNotes.create(formID=formId, createdBy=currentUser, date=currentDate, notesContents=stripresponse) # creates a new entry in the laborOfficeNotes table

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
        currentUser = require_login()
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
        print("Error Populating Overload Modal:", e)
        return render_template('errors/500.html', currentUser = currentUser), 500

@admin.route('/admin/releaseModal/<formHistoryID>', methods=['GET'])
def getReleaseModalData(formHistoryID):
    """
    This function will retrieve the data to populate the release modal.
    """
    try:
        currentUser = require_login()
        historyForm = FormHistory.select().where(FormHistory.formHistoryID == int(formHistoryID))
        noteTotal = AdminNotes.select().where(AdminNotes.formID == historyForm[0].formID.laborStatusFormID).count()
        return render_template('snips/pendingReleaseModal.html',
                                            historyForm = historyForm,
                                            formHistoryID = historyForm[0].formHistoryID,
                                            laborStatusFormID = historyForm[0].formID.laborStatusFormID,
                                            noteTotal = noteTotal
                                            )
    except Exception as e:
        print("Error Populating Release Modal:", e)
        return render_template('errors/500.html', currentUser = currentUser), 500

@admin.route('/admin/modalFormUpdate', methods=['POST'])
def modalFormUpdate():
    """
    This function will update the overload or release form based on the form
    type and the data from the modal.
    """
    try:
        currentUser = require_login()
        if not currentUser:
            return render_template('errors/403.html')

        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            historyForm = FormHistory.get(FormHistory.formHistoryID == rsp['formHistoryID'])
            email = emailHandler(historyForm.formHistoryID)
            currentDate = datetime.now().strftime("%Y-%m-%d")
            status = Status.get(Status.statusName == rsp['status'])
            if rsp['formType'] == 'Overload':
                overloadForm = OverloadForm.get(OverloadForm.overloadFormID == historyForm.overloadForm.overloadFormID)
                overloadForm.laborApproved = status.statusName
                overloadForm.laborApprover = currentUser
                overloadForm.laborReviewDate = currentDate
                overloadForm.save()
                try:
                    pendingForm = FormHistory.select().where((FormHistory.formID == historyForm.formID) & (FormHistory.status == "Pending")).get()
                    if historyForm.adjustedForm and rsp['status'] == "Approved":
                        LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == historyForm.formID)
                        if historyForm.adjustedForm.fieldAdjusted == "weeklyHours":
                            LSF.weeklyHours = pendingForm.adjustedForm.newValue
                            LSF.save()
                    if pendingForm.historyType.historyTypeName == "Labor Status Form" or (pendingForm.historyType.historyTypeName == "Labor Adjustment Form" and pendingForm.adjustedForm.fieldAdjusted == "weeklyHours"):
                        if status.statusName == "Approved Reluctantly":
                            pendingForm.status = "Approved"
                        else:
                            pendingForm.status = status.statusName
                        pendingForm.reviewedBy = currentUser
                        pendingForm.reviewedDate = currentDate
                        if 'denialReason' in rsp.keys():
                            pendingForm.rejectReason = rsp['denialReason']
                            AdminNotes.create(formID = pendingForm.formID.laborStatusFormID,
                                            createdBy = currentUser,
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
                                createdBy = currentUser,
                                date = currentDate,
                                notesContents = rsp['denialReason'])
            if 'adminNotes' in rsp.keys():
                # We only add admin notes if there was a note made on the UI
                AdminNotes.create(formID = historyForm.formID.laborStatusFormID,
                                createdBy = currentUser,
                                date = currentDate,
                                notesContents = rsp['adminNotes'])
            historyForm.status = status.statusName
            historyForm.reviewedBy = currentUser
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
