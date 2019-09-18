#from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
#from flask_login import current_user, login_required
from flask import flash, send_file, json, jsonify
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

@admin.route('/admin/pendingStatusForms', methods=['GET'])
def pendingForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')


        # pending_status_forms = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate)
        pending_labor_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Status Form").order_by(-FormHistory.createdDate)

        # # Logged in & Admin
        users = User.select()


        return render_template( 'admin/pendingStatusForms.html',
                                title=('Pending Forms'),
                                username=current_user.username,
                                users=users,
                                pending_labor_forms = pending_labor_forms
                                # pending_status_forms = pending_status_forms
                                # pending_modified_forms = pending_modified_forms,
                                # pending_release_forms = pending_release_forms,
                                # pending_overload_forms = pending_overload_forms
                                )

    except Exception as e:
        print(e)
        return render_template('errors/500.html')

@admin.route('/admin/checkedForms', methods=['POST'])
def approvedForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            print("Inserted into nonexistent Banner DB")
            #FIXME: Update form history
            approved_details = modal_aproval_data(rsp)
            print(approved_details, "before return")
            return jsonify(approved_details)
    except Exception as e:
        print("This did not work", e)
        return jsonify({"Success": False})

#method extracts data from the data base to papulate pending form approvale modal
def modal_aproval_data(approval_ids):
    id_list = []
    for student in approval_ids:
        student_details = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == int(student))
        student_firstname, student_lastname = student_details.studentSupervisee.FIRST_NAME, student_details.studentSupervisee.LAST_NAME
        student_name = str(student_firstname) + " " + str(student_lastname)
        # print(student_name)
        student_pos = student_details.POSN_TITLE
        supervisor_firstname, supervisor_lastname = student_details.supervisor.FIRST_NAME, student_details.supervisor.LAST_NAME
        supervisor_name = str(supervisor_firstname) +" "+ str(supervisor_lastname)
        print(supervisor_name)
        student_hours = student_details.weeklyHours
        student_hours_ch = student_details.contractHours
        temp_list = []
        temp_list.append(student_name)
        temp_list.append(student_pos)
        temp_list.append(student_hours)
        temp_list.append(supervisor_name)
        temp_list.append(student_hours_ch)
        id_list.append(temp_list)
    return(id_list)

@admin.route('/admin/finalApproval', methods=['POST'])
def finalApproval():
    try:
        rsp = eval(request.data.decode("utf-8"))
        for id in rsp:
            approving_labor_forms = FormHistory.get(FormHistory.formHistoryID == id)
            print("before approved \n" , approving_labor_forms.status.statusName)
            approving_labor_forms.status.statusName = "Approved"
            print("approved reached : \n", approving_labor_forms.status.statusName)
            approving_labor_forms.save()
         # return pendingForms()
    except Exception as e:
        print("final approval of the modal did not work", e)

@admin.route('/admin/getNotes/<formid>', methods=['GET'])
def getNotes(formid):
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')
        print(formid)
        notes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formid)
        print(notes)

        notesDict = {}
        if notes.supervisorNotes:
            notesDict["supervisorNotes"] = notes.supervisorNotes

        if notes.laborDepartmentNotes:
            notesDict["laborDepartmentNotes"] = notes.laborDepartmentNotes

        print(notesDict["supervisorNotes"])
        return jsonify(notesDict)

    except Exception as e:
        print("This did not work", e)
        return jsonify({"Success": False})
