from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.formHistory import *
from app.models.overloadForm import *
from app.models.student import *
from app.controllers.errors_routes.handlers import *
from app.login_manager import require_login
from flask import json
from flask import make_response
import datetime
from datetime import date
from app import cfg

@main_bp.route('/laborHistory/<id>', methods=['GET', 'POST'])
def laborhistory(id):
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')

        student = Student.get(Student.ID == id)
        studentForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == student)
        return render_template( 'main/laborhistory.html',
    				            title=('Labor History'),
                                student = student,
                                username=current_user.username,
                                studentForms = studentForms,
                              )
    except:
        render_template('errors/500.html')

@main_bp.route('/laborHistory/modal/<statusKey>', methods=['GET'])
def populateModal(statusKey):
    try:
        forms = FormHistory.select().where(FormHistory.formID == statusKey).order_by(FormHistory.createdDate.desc())
        print(forms)
        statusForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == statusKey)
        print(statusForm)
        currentDate = datetime.date.today()
        buttonState = None
        current_user = cfg['user']['debug']
        for form in forms:
            if current_user != (form.createdBy.username or form.formID.supervisor.username):
                break
            else:
                if form.releaseForm != None:
                    if form.status.statusName == "Approved":
                        buttonState = 0 #Only rehire button
                        break
                if form.overloadForm != None:
                    if form.status.statusName == "Pending":
                        buttonState = 1 #Only withdraw button
                        break
                if form.historyType.historyTypeName == "Labor Status Form":
                    if form.status.statusName == "Pending":
                        buttonState = 2 #Withdraw and modify buttons
                        break
                    elif form.status.statusName == "Denied":
                        buttonState = 0 #Rehire button
                        break
                    elif form.status.statusName == "Approved":
                        if currentDate <= form.formID.termCode.termEnd:
                            buttonState = 3 #Release, modify, and rehire buttons
                            break
                        elif currentDate > form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire
                            break
        resp = make_response(render_template('snips/studentHistoryModal.html',
                                            forms = forms,
                                            statusForm = statusForm,
                                            currentDate = currentDate,
                                            buttonState = buttonState
                                            ))
        return (resp)
    except Exception as e:
        print(e)
        render_template('errors/500.html')
        return (jsonify({"Success": False}))

@main_bp.route('/laborHistory/modal/updatestatus', methods=['POST'])
def updatestatus_post():
    try:
        print("im here")
        rsp = eval(request.data.decode("utf-8"))
        for key in rsp:
            overloadkey = FormHistory.get(FormHistory.formID == rsp[key]["formID"] and FormHistory.historyType == "Labor Overload Form")
            deleting_overload    = OverloadForm.get(OverloadForm.overloadFormID == overloadkey.overloadForm).delete_instance()
            deleting_formhisotry = FormHistory.get(FormHistory.formID == rsp[key]["formID"] and FormHistory.historyType == "Labor Overload Form").delete_instance()
        return jsonify({"Success": True})
    except Exception as e:
        print(e)
        return jsonify({"Success": False})
