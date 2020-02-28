#from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
#from flask_login import current_user, login_required
from flask import flash, send_file, json, jsonify, redirect, url_for
from app.login_manager import *
from app.controllers.admin_routes import admin
from app.controllers.errors_routes.handlers import *
from app.models.laborReleaseForm import LaborReleaseForm
from app.models.laborStatusForm import LaborStatusForm
from app.models.modifiedForm import ModifiedForm
from app.models.overloadForm import OverloadForm
from app.models.formHistory import *
from app.models.term import Term
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
        if formType  == "all":
            formList = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate).distinct()
            approvalTarget = "allFormsdenyModal"
            pageTitle = "All Pending Fomrs"
        else:
            if formType == "pendingLabor":
                historyType = "Labor Status Form"
                approvalTarget = "denyLaborStatusFormsModal"
                pageTitle = "Pending Labor Status Forms"

            elif formType == "pendingModified":
                historyType = "Modified Labor Form"
                approvalTarget = "denyModifiedFormsModal"
                pageTitle = "Pending Modified Forms"

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
                                isLaborAdmin = isLaborAdmin
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
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            approved_details =  modal_aproval_and_denial_data(rsp)
            return jsonify(approved_details)
    except Exception as e:
        print("error", e)
        return jsonify({"Success": False})

@admin.route('/admin/finalApproval', methods=['POST'])
def finalApproval():
    ''' This method changes the status of the pending forms to approved '''
    rsp = eval(request.data.decode("utf-8"))
    for id in rsp:
        history_type = FormHistory.get(FormHistory.formHistoryID == int(id))
        if str(history_type.historyType) == 'Labor Status Form':
            approving_labor_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Status Form')
            approving_labor_forms.status = Status.get(Status.statusName == "Approved")
            approving_labor_forms.reviewedDate = date.today()
            createdUser = User.get(username = cfg['user']['debug'])
            approving_labor_forms.reviewedBy = createdUser.UserID
            approving_labor_forms.save()
        elif str(history_type.historyType) == 'Modified Labor Form':
            approving_labor_modified_forms = FormHistory.get(FormHistory.formHistoryID== int(id), FormHistory.historyType == 'Modified Labor Form')
            approving_labor_modified_forms.status = Status.get(Status.statusName == "Approved")
            approving_labor_modified_forms.reviewedDate = date.today()
            createdUser = User.get(username = cfg['user']['debug'])
            approving_labor_modified_forms.reviewedBy = createdUser.UserID
            approving_labor_modified_forms.save()
        elif str(history_type.historyType) == 'Labor Overload Form':
            approving_labor_overload_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Overload Form')
            approving_labor_overload_forms.status = Status.get(Status.statusName == "Approved")
            approving_labor_overload_forms.reviewedDate = date.today()
            createdUser = User.get(username = cfg['user']['debug'])
            approving_labor_overload_forms.reviewedBy = createdUser.UserID
            approving_labor_overload_forms.save()
        elif str(history_type.historyType) == 'Labor Release Form':
            approving_labor_release_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Release Form')
            approving_labor_release_forms.status = Status.get(Status.statusName == "Approved")
            approving_labor_release_forms.reviewedDate = date.today()
            createdUser = User.get(username = cfg['user']['debug'])
            approving_labor_release_forms.reviewedBy = createdUser.UserID
            approving_labor_release_forms.save()
    return jsonify({"success": True})

@admin.route('/admin/finalDenial', methods=['POST'])
def finalDenial():
    ''' This method changes labor status pending forms to approved'''
    try:
        rsp = eval(request.data.decode("utf-8"))
        for id in rsp:
            history_type = FormHistory.get(FormHistory.formHistoryID == int(id))
            if str(history_type.historyType) == 'Labor Status Form':
                approving_labor_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Status Form')
                approving_labor_forms.status = Status.get(Status.statusName == "Denied")
                approving_labor_forms.reviewedDate = date.today()
                createdUser = User.get(username = cfg['user']['debug'])
                approving_labor_forms.reviewedBy = createdUser.UserID
                approving_labor_forms.save()
            elif str(history_type.historyType) == 'Modified Labor Form':
                approving_labor_modified_forms = FormHistory.get(FormHistory.formHistoryID== int(id), FormHistory.historyType == 'Modified Labor Form')
                approving_labor_modified_forms.status = Status.get(Status.statusName == "Denied")
                approving_labor_modified_forms.reviewedDate = date.today()
                createdUser = User.get(username = cfg['user']['debug'])
                approving_labor_modified_forms.reviewedBy = createdUser.UserID
                approving_labor_modified_forms.save()
            elif str(history_type.historyType) == 'Labor Overload Form':
                approving_labor_overload_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Overload Form')
                approving_labor_overload_forms.status = Status.get(Status.statusName == "Denied")
                approving_labor_overload_forms.reviewedDate = date.today()
                createdUser = User.get(username = cfg['user']['debug'])
                approving_labor_overload_forms.reviewedBy = createdUser.UserID
                approving_labor_overload_forms.save()
            elif str(history_type.historyType) == 'Labor Release Form':
                approving_labor_release_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Release Form')
                approving_labor_release_forms.status = Status.get(Status.statusName == "Denied")
                approving_labor_release_forms.reviewedDate = date.today()
                createdUser = User.get(username = cfg['user']['debug'])
                approving_labor_release_forms.reviewedBy = createdUser.UserID
                approving_labor_release_forms.save()
        return jsonify({"success": True})
    except Exception as e:
        print("error", e)
        return jsonify({"success": False})

#method extracts data from the data base to papulate pending form approvale modal
def modal_aproval_and_denial_data(approval_ids):
    ''' This method grabs the data that populated the on approve modal for lsf'''
    id_list = []
    for form_history_id in approval_ids:
        fhistory_id = LaborStatusForm.select().join(FormHistory).where(FormHistory.formHistoryID == int(form_history_id)).get()
        student_details = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == fhistory_id)
        student_firstname, student_lastname = student_details.studentSupervisee.FIRST_NAME, student_details.studentSupervisee.LAST_NAME
        student_name = str(student_firstname) + " " + str(student_lastname)
        student_pos = student_details.POSN_TITLE
        supervisor_firstname, supervisor_lastname = student_details.supervisor.FIRST_NAME, student_details.supervisor.LAST_NAME
        supervisor_name = str(supervisor_firstname) +" "+ str(supervisor_lastname)
        student_hours = student_details.weeklyHours
        student_hours_ch = student_details.contractHours
        temp_list = []
        temp_list.append(student_name)
        temp_list.append(student_pos)
        temp_list.append(supervisor_name)
        temp_list.append(str(student_hours))
        temp_list.append(str(student_hours_ch))
        id_list.append(temp_list)
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
        notes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formid)
        notesDict = {}
        if notes.supervisorNotes:
            notesDict["supervisorNotes"] = notes.supervisorNotes

        if notes.laborDepartmentNotes:
            listOfNotes = json.loads(notes.laborDepartmentNotes)
            notesDict["laborDepartmentNotes"] = ""
            for i in listOfNotes:
                singleNote = "<p>" + i + "</p>"
                notesDict["laborDepartmentNotes"] = notesDict["laborDepartmentNotes"] + singleNote
        return jsonify(notesDict)

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
        current_user_string = str(" - From: " + current_user.FIRST_NAME[0] + "." + " " + current_user.LAST_NAME) #Getting the name of the current user in a string and formatting it for the note.  Up for change, we'll demo it
        rsp = eval(request.data.decode("utf-8"))
        #print(rsp)
        notes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formId)
        #print(notes)
        laborDeptNotes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formId)
        #print(laborDeptNotes)
        print(rsp)
        if rsp:
            rsp = rsp + current_user_string #adding the name of the user to the rsp that is the note.
            listOfNotes = [rsp]
            #print(listOfNotes)
            #print(current_user_string)
            for i in listOfNotes:
                i = i + current_user_string
            print(listOfNotes)
            if notes.laborDepartmentNotes != None:
                listOfNotesJson = json.loads(notes.laborDepartmentNotes)
                for i in listOfNotesJson:
                    listOfNotes.append(i)
            listOfNotesJson = json.dumps(listOfNotes)
            #print(listOfNotesJson)
            laborDeptNotes.laborDepartmentNotes = listOfNotesJson
            #print(laborDeptNotes)
            laborDeptNotes.save() #Updates labor notes
            return jsonify({"Success": True})

        elif rsp=="" or rsp==None or " -    " in rsp:
            flash("No changes made to notes.", "danger")
            return jsonify({"Success": False})

    except Exception as e:
        print("error", e)
        return jsonify({"Success": False})
