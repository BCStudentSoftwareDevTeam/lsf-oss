#from flask import render_template  #, redirect, url_for, request, g, jsonify, current_app
#from flask_login import current_user, login_required
from flask import flash, send_file
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

@admin.route('/admin/pendingStatusForms', methods=['GET', 'POST'])
def pendingForms():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')


        # pending_status_forms = FormHistory.select().where(FormHistory.status == "Pending").order_by(-FormHistory.createdDate)
        pending_labor_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Status Form").order_by(-FormHistory.createdDate)
        # pending_release_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Release Form").order_by(-FormHistory.createdDate)
        # pending_overload_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Labor Overload Form").order_by(-FormHistory.createdDate)
        # pending_modified_forms = FormHistory.select().where(FormHistory.status == "Pending").where(FormHistory.historyType == "Modified Labor Form").order_by(-FormHistory.createdDate)
        #
        # pendingModifiedList = []
        # for i in pending_labor_forms:
        #     print(str(i) + " this should be 1")
        #
        # for i in pending_release_forms:
        #     print(str(i) + " this should be 7")
        #
        # for i in pending_overload_forms:
        #     print(str(i) + "this should be 11")
        #
        # for i in pending_modified_forms:
        #     pendingModifiedList.append(i)
        #     print(pendingModifiedList)
        #
        #
        #
        # #print(len(pending_status_forms))
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
