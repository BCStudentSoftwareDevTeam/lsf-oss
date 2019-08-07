from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app, send_file
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
from app.controllers.main_routes.download import ExcelMaker

@main_bp.route('/laborHistory/<id>', methods=['GET'])
def laborhistory(id):
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')

        student = Student.get(Student.ID == id)
        studentForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == student)
        formHistoryList = ""
        for form in studentForms:
            formHistoryList = formHistoryList + str(form.laborStatusFormID) + ","
        formHistoryList = formHistoryList[0:-1]
        return render_template( 'main/formHistory.html',
    				            title=('Labor History'),
                                student = student,
                                username=current_user.username,
                                studentForms = studentForms,
                                formHistoryList = formHistoryList
                              )
    except:
        return render_template('errors/500.html')

@main_bp.route("/laborHistory/download" , methods=['POST'])
def downloadFormHistory():
    try:
        data = request.form
        historyList = data["listOfForms"].split(',')
        excel = ExcelMaker()
        completePath = excel.makeExcelStudentHistory(historyList)
        filename = completePath.split('/').pop()
        return send_file(completePath, mimetype='text/csv', as_attachment=True, attachment_filename=filename)
    except:
        return render_template('errors/500.html')

@main_bp.route('/laborHistory/modal/<statusKey>', methods=['GET'])
def populateModal(statusKey):
    try:
        forms = FormHistory.select().where(FormHistory.formID == statusKey).order_by(FormHistory.createdDate.desc())
        statusForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == statusKey)
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
                    elif form.status.statusName == "Pending":
                        buttonState = None # no buttons
                        break
                    elif form.status.statusName == "Denied":
                        buttonState = 3   #Release, modify, and rehire buttons
                        break
                if form.overloadForm != None:
                    if form.status.statusName == "Pending":
                        buttonState = 1 #Only withdraw button
                        break
                if form.modifiedForm != None:
                    if form.status.statusName == "Pending":
                        buttonState = None # no buttons
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
        return render_template('errors/500.html')
        return (jsonify({"Success": False}))

@main_bp.route('/laborHistory/modal/updatestatus', methods=['POST'])
def updatestatus_post():
    try:
        rsp = eval(request.data.decode("utf-8"))
        overloadkey = FormHistory.select().where(FormHistory.formID == rsp["FormID"])
        student = LaborStatusForm.get(rsp["FormID"]).studentSupervisee.ID
        count = 0
        for key in overloadkey:
            count += 1
        print(count)
        if count == 1: #means they have only have pending labor status form
             deleteFormHistoryStatus = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Status Form").delete_instance() #delete the form history for the LSF
             deleteLaborStatusForm   = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == rsp["FormID"]).delete_instance() #delete the status form as well
        elif count == 2: # means they have a pending labor status form and overload form
            overloadformid            = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Overload Form")
            deleteOverloadForm        = OverloadForm.get(OverloadForm.overloadFormID == overloadformid.overloadForm).delete_instance()
            deleteFormHistoryOverload = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Overload Form").delete_instance()
            deleteFormHistoryStatus   = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Status Form").delete_instance()
            deleteLaborStatusForm     = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == rsp["FormID"]).delete_instance()
        elif count == 3: # means they have 3 pending forms (modified form, lsf, labor overload form)
            modifiedformid            = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Modified Labor Form")
            deletemodifiedForm        = ModifiedForm.get(ModifiedForm.modifiedFormID == modifiedformid.modifiedForm).delete_instance()
            deleteFormHistoryModified = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Modified Labor Form").delete_instance()
            overloadformid            = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Overload Form")
            deleteOverloadForm        = OverloadForm.get(OverloadForm.overloadFormID == overloadformid.overloadForm).delete_instance()
            deleteFormHistoryOverload = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Overload Form").delete_instance()


        #     selectedFormHistory = FormHistory.select().where(FormHistory.formHistoryID == key)
        # if selectedFormHistory.status == "Pending" and selectedFormHistory.overloadForm == None: #The selected form history's status is pending
        #     deleteFormHistoryStatus = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Status Form").delete_instance() #delete the form history for the LSF
        #     deleteLaborStatusForm        = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == rsp["FormID"]).delete_instance() #delete the status form as well
        # elif selectedFormHistory.status == "Pending" and selectedFormHistory.overloadForm != None:

    #     for i in selectedFormHistory:
    #         deleteOverloadForm    = OverloadForm.get(OverloadForm.overloadFormID == i.overloadForm).delete_instance()
    #     deleteFormHistoryOverload = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Overload Form").delete_instance()
    #     deleteFormHistoryStatus = FormHistory.get(FormHistory.formID == rsp["FormID"] and FormHistory.historyType == "Labor Status Form").delete_instance()
    #     deleteLaborStatusForm        = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == rsp["FormID"]).delete_instance()
        flash("Your selected form has been withdrawn.", "success")
        return jsonify({"Success":True, "url":"/laborHistory/" + student})
    except Exception as e:
        print(e)
        return jsonify({"Success": False})
