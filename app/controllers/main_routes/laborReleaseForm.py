from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborReleaseForm import *
from app.models.formHistory import *
from app.models.laborStatusForm import *
from flask_bootstrap import bootstrap_find_resource
from app.models.student import *
from app.models.department import *
from app.models.historyType import *
from app.models.user import *
from app.controllers.errors_routes.handlers import *
from app.login_manager import require_login
from flask import Flask, redirect, url_for, flash
from flask import request
from datetime import datetime, date

@main_bp.route('/laborReleaseForm/<laborStatusKey>', methods=['GET', 'POST'])
# @main_bp.route('/laborReleaseForm', methods=['GET', 'POST'])
# @login_required

def laborReleaseForm(laborStatusKey):
    current_user = require_login()
    if not current_user:
        render_template("errors/403.html")
    if not current_user.isLaborAdmin:
        render_template("errors/403.html")

    students = Student.select()
    department = Department.select()
    users = User.select()
    forms = LaborStatusForm.select().distinct().where(LaborStatusForm.laborStatusFormID == laborStatusKey)


    if(request.method == 'POST'):
        try:
            historyForms = FormHistory.select().where((FormHistory.formID == laborStatusKey) & (FormHistory.releaseForm != None))
            if historyForms:
                for form in historyForms:
                    if form.status.statusName != "Denied":
                        flash("An error has occurred. Student already has a 'Pending' labor release form.", "danger")
                        return redirect(url_for("main.index"))
            datepickerDate = request.form.get("date")
            releaseDate = datetime.strptime(datepickerDate, "%m/%d/%Y").strftime("%Y-%m-%d")
            releaseReason = request.form.get("notes")
            releaseCondition = request.form.get("condition")

            newLaborReleaseForm = LaborReleaseForm.create(
                                        conditionAtRelease = releaseCondition,
                                        releaseDate = releaseDate,
                                        reasonForRelease = releaseReason
                                        )

            historytype = HistoryType.get(HistoryType.historyTypeName == "Labor Release Form")
            status = Status.get(Status.statusName == "Pending")
            laborStatusForiegnKey = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)

            newFormHistory = FormHistory.create(
                                        formID = laborStatusForiegnKey.laborStatusFormID,
                                        historyType = historytype.historyTypeName,
                                        releaseForm = newLaborReleaseForm.laborReleaseFormID,
                                        modifiedForm = None,
                                        overloadForm = None,
                                        createdBy = current_user.username,
                                        createdDate = date.today(),
                                        reviewedDate = None,
                                        reviewedBy = None,
                                        status = status.statusName,
                                        rejectReason = None
                                        )
            flash("Your labor release form has been submitted.", "success")
            return redirect(url_for("main.index"))

        except Exception as e:
            print(e)
            flash("An error has occurred. Your labor release form was not submitted.", "danger")
            return redirect(url_for("main.index"))

    return render_template('main/laborReleaseForm.html',
				            title=('Labor Release Form'),
                            students = students,
                            department = department,
                            users = users,
                            forms = forms
                          )
