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
from flask import Flask, redirect, url_for, flash

#       ALL PENDING FORMS       #
@admin.route('/admin/allPendingForms',  methods=['GET'])
def allPendingForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        all_pending_forms = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate)
        users = User.select()

        return render_template( 'admin/allPendingForms.html',
                                title=('All Pending Forms'),
                                username=current_user.username,
                                users=users,
                                all_pending_forms = all_pending_forms
                                )
    except Exception as e:
        print(e)
        return render_template('errors/500.html')

#        PENDING LABOR STATUS FORMS         #
@admin.route('/admin/pendingStatusForms',  methods=['GET'])
def pendingForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        pending_labor_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Status Form").order_by(-FormHistory.createdDate)
        pending_modified_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Modified Labor Form").order_by(-FormHistory.createdDate)
        pending_overload_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Overload Form").order_by(-FormHistory.createdDate)
        pending_release_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Release Form").order_by(-FormHistory.createdDate)
        all_pending_forms = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate)

        # print(pending_labor_forms)
        users = User.select()

        return render_template( 'admin/pendingStatusForms.html',
                                title=('Pending Forms'),
                                username=current_user.username,
                                users=users,
                                all_pending_forms = all_pending_forms,
                                pending_labor_forms = pending_labor_forms,
                                pending_modified_forms = pending_modified_forms,
                                pending_overload_forms = pending_overload_forms,
                                pending_release_forms = pending_release_forms
                                )
    except Exception as e:
        print(e)
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

        print("Test")
        pending_modified_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Modified Labor Form").order_by(-FormHistory.createdDate)                # # Logged in & Admin
        print("I'm here")
        print(pending_modified_forms)
        users = User.select()

        return render_template( 'admin/pendingModifiedForms.html',
                                username=current_user.username,
                                users=users,
                                pending_modified_forms = pending_modified_forms
                                )
    except Exception as e:
        print(e)
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
        print(e)
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
        print(e)
        return render_template('errors/500.html')

@admin.route('/admin/checkedForms', methods=['POST'])
def approvedForms():
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
        # print(rsp)
        if rsp:
            print("Inserted into nonexistent Banner DB")
            #FIXME: Update form history

            return jsonify({"Success": True})
    except Exception as e:
        print("This did not work", e)
        return jsonify({"Success": False})


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
        # print(rsp)
        laborDeptNotes =  LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formId)
        # print(laborDeptNotes)

        if rsp:
            laborDeptNotes.laborDepartmentNotes = rsp
            laborDeptNotes.save() #Updates labor notes


            print("This freggin' worked omg")
            flash("Notes Saved", "success")
            return jsonify({"Success": True})
    except Exception as e:
        print("This ain't work", e)
        return jsonify({"Success": False})
