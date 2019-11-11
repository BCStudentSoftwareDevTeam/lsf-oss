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
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash

#       ALL PENDING FORMS       #
@admin.route('/admin/allPendingForms',  methods=['GET'])
@admin.route('/admin/pendingForms/<formType>',  methods=['GET'])
def allPendingForms():
    try:
        current_user = require_login()

        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        formList = None
        historyType = None 
        approvalTarget = ""
        if formType  == "all":
            formList = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate).distinct()
        else:

            if formType == "labor"
        pending_labor_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Status Form").order_by(-FormHistory.createdDate).distinct()
        pending_modified_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Modified Labor Form").order_by(-FormHistory.createdDate).distinct()
        pending_overload_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Overload Form").order_by(-FormHistory.createdDate).distinct()
        pending_release_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Release Form").order_by(-FormHistory.createdDate).distinct()
        all_pending_forms = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate).distinct()

        # print(pending_labor_forms)
        users = User.select()

        return render_template( 'admin/allPendingForms.html',

                                title=('All Pending Forms'),
                                username=current_user.username,
                                users=users,
                                all_pending_forms = all_pending_forms,
                                pending_labor_forms = pending_labor_forms,
                                pending_modified_forms = pending_modified_forms,
                                pending_overload_forms = pending_overload_forms,
                                pending_release_forms = pending_release_forms
                                )
    except Exception as e:
        print("All Pending", e)
        return render_template('errors/500.html')

#        PENDING STATUS FORMS         #
@admin.route('/admin/pendingStatusForms',  methods=['GET'])
def pendingStatusForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        print("Test")
        pending_labor_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Status Form").order_by(-FormHistory.createdDate)                # # Logged in  Admin
        print("I'm here")
        users = User.select()

        return render_template( 'admin/pendingStatusForms.html',
                                username=current_user.username,
                                users=users,
                                pending_labor_forms = pending_labor_forms
                                )
    except Exception as e:
        print("Pending Status", e)
        return render_template('errors/500.html')

#        PENDING MODIFIED FORMS         #
@admin.route('/admin/pendingModifiedForms',  methods=['GET'])
def pendingModifiedForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        pending_modified_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Modified Labor Form").order_by(-FormHistory.createdDate)                # # Logged in & Admin
        users = User.select()

        return render_template( 'admin/pendingModifiedForms.html',
                                username=current_user.username,
                                users=users,
                                pending_modified_forms = pending_modified_forms
                                )
    except Exception as e:
        print("Pending Modified", e)
        return render_template('errors/500.html')

#        PENDING OVERLOAD FORMS         #
@admin.route('/admin/pendingOverloadForms',  methods=['GET'])
def pendingOverloadForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        pending_overload_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Overload Form").order_by(-FormHistory.createdDate)
        users = User.select()

        return render_template( 'admin/pendingOverloadForms.html',
                                username=current_user.username,
                                users=users,
                                pending_overload_forms = pending_overload_forms
                                )
    except Exception as e:
        print("Pending Overload", e)
        return render_template('errors/500.html')

#        PENDING RELEASE FORMS         #
@admin.route('/admin/pendingReleaseForms.html',  methods=['GET'])
def pendingReleaseForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        pending_release_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Release Form").order_by(-FormHistory.createdDate)
        users = User.select()

        return render_template( 'admin/pendingReleaseForms.html',
                                username=current_user.username,
                                users=users,
                                pending_release_forms = pending_release_forms
                                )
    except Exception as e:
        print("Pending Release", e)
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
            #FIXME: Update form history
            approved_details =  modal_aproval_and_denial_data(rsp)
            return jsonify(approved_details)
    except Exception as e:
        print("This did not work", e)
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
            approving_labor_forms.save()
        elif str(history_type.historyType) == 'Modified Labor Form':
            approving_labor_modified_forms = FormHistory.get(FormHistory.formHistoryID== int(id), FormHistory.historyType == 'Modified Labor Form')
            approving_labor_modified_forms.status = Status.get(Status.statusName == "Approved")
            approving_labor_modified_forms.save()
        elif str(history_type.historyType) == 'Labor Overload Form':
            approving_labor_overload_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Overload Form')
            approving_labor_overload_forms.status = Status.get(Status.statusName == "Approved")
            approving_labor_overload_forms.save()
        elif str(history_type.historyType) == 'Labor Release Form':
            approving_labor_release_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Release Form')
            approving_labor_release_forms.status = Status.get(Status.statusName == "Approved")
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
                approving_labor_forms.save()
            elif str(history_type.historyType) == 'Modified Labor Form':
                approving_labor_modified_forms = FormHistory.get(FormHistory.formHistoryID== int(id), FormHistory.historyType == 'Modified Labor Form')
                approving_labor_modified_forms.status = Status.get(Status.statusName == "Denied")
                approving_labor_modified_forms.save()
            elif str(history_type.historyType) == 'Labor Overload Form':
                approving_labor_overload_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Overload Form')
                approving_labor_overload_forms.status = Status.get(Status.statusName == "Denied")
                approving_labor_overload_forms.save()
            elif str(history_type.historyType) == 'Labor Release Form':
                approving_labor_release_forms = FormHistory.get(FormHistory.formHistoryID == int(id), FormHistory.historyType == 'Labor Release Form')
                approving_labor_release_forms.status = Status.get(Status.statusName == "Denied")
                approving_labor_release_forms.save()
        return jsonify({"success": True})
    except Exception as e:
        print("final approval of the modal did not work", e)
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
        print(supervisor_name)
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
        print(formid)
        notes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formid)
        #print(notes)

        notesDict = {}
        if notes.supervisorNotes:
            notesDict["supervisorNotes"] = notes.supervisorNotes

        if notes.laborDepartmentNotes:
            notesDict["laborDepartmentNotes"] = notes.laborDepartmentNotes
        # print(notesDict["supervisorNotes"])
        # print(notesDict["laborDepartmentNotes"])
        return jsonify(notesDict)

    except Exception as e:
        print("This did not work", e)
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
        print(rsp)
        laborDeptNotes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formId)
        # print(laborDeptNotes)

        if rsp:
            laborDeptNotes.laborDepartmentNotes = rsp
            # print(type(rsp))
            laborDeptNotes.save() #Updates labor notes

            print("This freggin' worked omg")
            return jsonify({"Success": True})

        elif rsp=="" or rsp==None:
            # print("reached")
            flash("No changes made to notes.", "danger")
            return jsonify({"Success": False})

    except Exception as e:
        print("This ain't work", e)
        return jsonify({"Success": False})
