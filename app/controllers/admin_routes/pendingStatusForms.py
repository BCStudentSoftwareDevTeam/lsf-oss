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
        print(notes)

        notesDict = {}
        if notes.supervisorNotes:
            notesDict["supervisorNotes"] = notes.supervisorNotes

        if notes.laborDepartmentNotes:
            notesDict["laborDepartmentNotes"] = notes.laborDepartmentNotes


        print(notesDict)
        # print(notesDict["supervisorNotes"])
        # print(notesDict["laborDepartmentNotes"])
        return jsonify(notesDict)


    except Exception as e:
        print("This did not work", e)
        return jsonify({"Success": False})


@admin.route('/admin/notesInsert/<formid>', methods=['POST'])
def insertNotes(formid):
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
        notes =  LaborStatusForm.get(LaborStatusForm.laborDepartmentNotes == formid)
        print(notes)

        print(data)
        if rsp:
            for data in rsp.values():
                pass
            #         pending_labor_forms



            #FIXME: Update form history

            return jsonify({"Success": True})
    except Exception as e:
        print("This did not work", e)
        return jsonify({"Success": False})
