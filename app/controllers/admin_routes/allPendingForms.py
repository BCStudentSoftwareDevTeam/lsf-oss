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
                                releaseFormCounter = releaseFormCounter
                                )
    except Exception as e:
        print("error", e)
        return render_template('errors/500.html')

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
        print("error", e)
        return jsonify({"Success": False})

@admin.route('/admin/updateStatus/<raw_status>', methods=['POST'])
def finalUpdateStatus(raw_status):
    ''' This method changes the status of the pending forms to approved '''

    if raw_status == 'approved':
        new_status = "Approved"
    elif raw_status == 'denied':
        new_status = "Denied"
    else:
        print("Unknown status: ", raw_status)
        return jsonify({"success": False})

    try:
        createdUser = User.get(username = cfg['user']['debug'])
        rsp = eval(request.data.decode("utf-8"))
        denyReason = None
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
            labor_forms.rejectReason = denyReason
    except Exception as e:
        print("Error preparing form for status update:",type(e).__name__ + ":", e)
        return jsonify({"success": False})

    # BANNER
    save_status = True # default true so that we will save in the Deny case
    if new_status == 'Approved':
        try:
            banner_data = prep_banner_data(labor_forms)
            conn = Banner()
            result = conn.insert(banner_data)
            save_status = (result == None)

        except Exception as e:
            print("Unable to update BANNER:",type(e).__name__ + ":", e)
            save_status = False

        else:
            save_status = True

    if save_status:
        labor_forms.save()
        return jsonify({"success": True})
    else:
        print("Unable to update form status.")
        return jsonify({"success": False})

def prep_banner_data(form):
    return []

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
        print("error", e)
        return jsonify({"Success": False})

@admin.route('/admin/overloadModal', methods=['POST'])
def getOverloadModalData():
    """
    This function will retrieve the data to populate the overload modal
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            overloadModalInfo = {}
            historyForm = FormHistory.get(FormHistory.formHistoryID == int(rsp[0]))
            studentFirstName, studentLastName = historyForm.formID.studentSupervisee.FIRST_NAME, historyForm.formID.studentSupervisee.LAST_NAME
            studentName = studentFirstName + " " + studentLastName
            studentPosition = historyForm.formID.POSN_TITLE
            studentHours = historyForm.formID.weeklyHours
            studentDepartment = historyForm.formID.department.DEPT_NAME
            studentSupervisorFirstName, studentSupervisorLastName  = historyForm.formID.supervisor.FIRST_NAME, historyForm.formID.supervisor.LAST_NAME
            studentSupervisorName = studentSupervisorFirstName + ' ' + studentSupervisorLastName
            studentOverloadReason = historyForm.overloadForm.studentOverloadReason
            try:
                SAASStatus = historyForm.overloadForm.SAASApproved.statusName
                SAASLastEmail = EmailTracker.select().limit(1).where((EmailTracker.recipient == 'SAAS') & (EmailTracker.formID == historyForm.formID.laborStatusFormID)) .order_by(EmailTracker.date.desc())
                SAASEmailDate = SAASLastEmail[0].date.strftime('%m/%d/%y')
            except (AttributeError, IndexError):
                # We expect to see the AttributeError and IndexError if there is no data,
                # and in those cases we set the variables manually
                SAASStatus = 'None'
                SAASEmailDate = 'No Email Sent'
            try:
                financialAidStatus = historyForm.overloadForm.financialAidApproved.statusName
                financialAidLastEmail = EmailTracker.select().limit(1).where((EmailTracker.recipient == 'Financial Aid') & (EmailTracker.formID == historyForm.formID.laborStatusFormID)) .order_by(EmailTracker.date.desc())
                financialAidEmailDate = financialAidLastEmail[0].date.strftime('%m/%d/%y')
            except (AttributeError, IndexError):
                financialAidStatus = 'None'
                financialAidEmailDate = 'No Email Sent'
            overloadModalInfo.update({
                                'stuName': studentName,
                                'stuPosition': studentPosition,
                                'stuDepartment': studentDepartment,
                                'stuSupervisor': studentSupervisorName,
                                'stuHours': studentHours,
                                'studentOverloadReason': studentOverloadReason,
                                'SAASEmail': SAASEmailDate,
                                'SAASStatus': SAASStatus,
                                'financialAidStatus': financialAidStatus,
                                'financialAidLastEmail': financialAidEmailDate
                                })
            return jsonify(overloadModalInfo)
    except Exception as e:
        print("error", e)
        return jsonify({"Success": False})

@admin.route('/admin/overloadFormUpdate', methods=['POST'])
def updateOverloadForm():
    """
    This function will retrieve update the overloaf from using the
    data entered into the modal.
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            historyForm = FormHistory.get(FormHistory.formHistoryID == rsp['formHistoryID'])
            overloadForm = OverloadForm.get(OverloadForm.overloadFormID == historyForm.overloadForm.overloadFormID)
            currentDate = datetime.now().strftime("%Y-%m-%d")
            createdUser = User.get(username = cfg['user']['debug'])
            status = Status.get(Status.statusName == rsp['status'])
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
            overloadForm.laborApproved = status.statusName
            overloadForm.laborApprover = createdUser.UserID
            overloadForm.laborReviewDate = currentDate
            overloadForm.save()
            historyForm.status = status.statusName
            historyForm.reviewedBy = createdUser.UserID
            historyForm.reviewedDate = currentDate
            historyForm.save()

            return jsonify({"Success": True})
    except Exception as e:
        print("error", e)
        return jsonify({"Success": False})

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
            # link = '/admin/financialAidOverloadApproval/' + str(rsp['formHistoryID'])
            # email = emailHandler(historyForm.historyFormID)
            # email.overloadVerification(recipient, link)
            currentDate = datetime.now().strftime('%m/%d/%y')
            newEmailInformation = {'recipient': recipient,
                                    'emailDate': currentDate,
                                    'status': 'Pending'
            }
            return jsonify(newEmailInformation)
    except Exception as e:
        print("error", e)
        return jsonify({"Success": False})
