from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app, send_file
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.formHistory import *
from app.models.overloadForm import *
from app.models.department import *
from app.models.student import *
from app.controllers.errors_routes.handlers import *
from app.login_manager import require_login
from flask import json
from flask import make_response
import datetime
from datetime import date
from app import cfg
from app.controllers.main_routes.download import ExcelMaker
from fpdf import FPDF
from app.logic.authorizationFunctions import*
from app.models.Tracy.stuposn import STUPOSN
from app.logic.buttonStatus import ButtonStatus

@main_bp.route('/laborHistory/<id>', methods=['GET'])
def laborhistory(id):
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:
            isLaborAdmin = False
            authorizedUser, departmentsList = laborHistoryAuthorizeUser(id, current_user.UserID)
            if authorizedUser == False:
                return render_template('errors/403.html')
        else:
            isLaborAdmin = True
            departmentsList = []
        student = Student.get(Student.ID == id)
        studentForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == student).order_by(LaborStatusForm.startDate.desc())
        formHistoryList = ""
        for form in studentForms:
            formHistoryList = formHistoryList + str(form.laborStatusFormID) + ","
        formHistoryList = formHistoryList[0:-1]
        return render_template( 'main/formHistory.html',
    				            title=('Labor History'),
                                student = student,
                                username=current_user.username,
                                studentForms = studentForms,
                                formHistoryList = formHistoryList,
                                departmentsList = departmentsList,
                                isLaborAdmin = isLaborAdmin
                              )
    except Exception as e:
        return render_template('errors/500.html')

@main_bp.route("/laborHistory/download" , methods=['POST'])
def downloadFormHistory():
    """
    This function is called when the download button is pressed.  It runs a function for writing to an excel sheet that is in download.py.
    This function downloads the created excel sheet of the history from the page.
    """
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
    """
    This function creates the modal and populates it with the history of a selected position.  It works with the openModal() function in laborhistory.js
    to create the modal, and append all of the data gathered here form the database to the modal.  It also sets a button state which decides which buttons
    to put on the modal depending on what form is in the history.
    """
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        forms = FormHistory.select().where(FormHistory.formID == statusKey).order_by(FormHistory.createdDate.desc(), FormHistory.formHistoryID.desc())
        statusForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == statusKey)
        currentDate = datetime.date.today()
        pendingformType = None
        buttonState = None
        current_user = current_user
        for form in forms:
            if form.adjustedForm != None:  # If a form has been adjusted then we want to retrieve supervisors names using the new and old values stored in adjusted table
                if form.adjustedForm.fieldAdjusted == "Supervisor": # if supervisor field in adjust forms has been changed,
                    newSupervisorID = form.adjustedForm.newValue    # use the supervisor pidm in the field adjusted to find supervisor in User table.
                    newSupervisor = User.get(User.UserID == newSupervisorID)
                    # we are temporarily storing the supervisor name in new value,
                    # because we want to show the supervisor name in the hmtl template.
                    form.adjustedForm.oldValue = form.formID.supervisor.FIRST_NAME + " " + form.formID.supervisor.LAST_NAME # old supervisor name
                    form.adjustedForm.newValue = newSupervisor.FIRST_NAME +" "+ newSupervisor.LAST_NAME
                if form.adjustedForm.fieldAdjusted == "Position": # if position field has been changed in adjust form then retriev position name.
                    newPositionCode = form.adjustedForm.newValue
                    newPosition = STUPOSN.get(STUPOSN.POSN_CODE == newPositionCode)
                    # temporarily storing the new position name in new value, and old position name in old value
                    # because we want to show these information in the hmtl template.
                    form.adjustedForm.newValue = form.formID.POSN_TITLE + " (" + form.formID.WLS+")"
                    form.adjustedForm.oldValue = newPosition.POSN_TITLE + " (" + newPosition.WLS+")"
        for form in forms:
            if current_user.username != (form.createdBy.username or form.formID.supervisor.username):
                buttonState = ButtonStatus.no_buttons
                break
            else:
                if form.releaseForm != None:
                    if form.status.statusName == "Approved":
                        if currentDate <= form.formID.endDate:
                            buttonState = ButtonStatus.show_rehire_button
                            break
                        elif currentDate > form.formID.endDate:
                            buttonState = ButtonStatus.show_rehire_button
                            break
                    elif form.status.statusName == "Pending":
                        buttonState = ButtonStatus.no_buttons_pending_forms
                        pendingformType = form.historyType.historyTypeName
                        break
                    elif form.status.statusName == "Denied":
                        if currentDate <= form.formID.endDate:
                            buttonState = ButtonStatus.show_release_adjustment_rehire_buttons
                            break
                        elif currentDate > form.formID.endDate:
                            buttonState = ButtonStatus.show_rehire_button
                            break
                if form.overloadForm != None:
                    if form.status.statusName == "Pending":
                        buttonState = ButtonStatus.show_withdraw_modify_buttons
                        break
                    if form.status.statusName == "Denied":
                        if currentDate <= form.formID.endDate:
                            buttonState = ButtonStatus.show_rehire_button
                            break
                        elif currentDate > form.formID.endDate:
                            buttonState = ButtonStatus.show_rehire_button
                            break
                if form.adjustedForm != None:
                    if form.status.statusName == "Pending":
                        buttonState = ButtonStatus.no_buttons_pending_forms
                        pendingformType = form.historyType.historyTypeName
                        break
                if form.historyType.historyTypeName == "Labor Status Form":
                    if form.status.statusName == "Pending":
                        buttonState = ButtonStatus.show_withdraw_modify_buttons
                        break
                    elif form.status.statusName == "Denied":
                        if currentDate <= form.formID.endDate:
                            buttonState = ButtonStatus.show_rehire_button
                            break
                        elif currentDate > form.formID.endDate:
                            buttonState = ButtonStatus.show_rehire_button
                            break
                    elif form.status.statusName == "Approved":
                        if currentDate <= form.formID.endDate:
                            if currentDate > form.formID.termCode.adjustmentCutOff:
                                buttonState = ButtonStatus.show_release_rehire_buttons
                                break
                            else:
                                buttonState = ButtonStatus.show_release_adjustment_rehire_buttons
                                break
                        else:
                            buttonState = ButtonStatus.show_rehire_button
                            break
        resp = make_response(render_template('snips/studentHistoryModal.html',
                                            forms = forms,
                                            statusForm = statusForm,
                                            currentDate = currentDate,
                                            buttonState = buttonState,
                                            pendingformType = pendingformType,
                                            ButtonStatus = ButtonStatus
                                            ))
        return (resp)
    except Exception as e:
        print("Error on button state: ", e)
        return (jsonify({"Success": False}))

@main_bp.route('/laborHistory/modal/printPdf/<statusKey>', methods=['GET'])
def ConvertToPDF(statusKey):
    """
    This function returns
    """
    try:
        forms = FormHistory.select().where(FormHistory.formID == statusKey).order_by(FormHistory.createdDate.desc())
        statusForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == statusKey)
        pdf = make_response(render_template('main/pdfTemplate.html',
                        forms = forms,
                        statusForm = statusForm
                        ))
        return (pdf)
    except Exception as e:
        return(jsonify({"Success": False}))


@main_bp.route('/laborHistory/modal/withdrawform', methods=['POST'])
def withdraw_form():
    """
    This function deletes forms from the database when they are pending and the "withdraw" button is clicked.
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        student = LaborStatusForm.get(rsp["FormID"])
        selectedPendingForms = FormHistory.select().join(Status).where(FormHistory.formID == rsp["FormID"]).where(FormHistory.status.statusName == "Pending").order_by(FormHistory.historyType.asc())
        for form in selectedPendingForms:
            if form.historyType.historyTypeName == "Labor Status Form":
                historyFormToDelete = FormHistory.get(FormHistory.formHistoryID == form.formHistoryID)
                laborStatusFormToDelete = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == form.formID.laborStatusFormID)
                historyFormToDelete.delete_instance()
                laborStatusFormToDelete.delete_instance()
            elif form.historyType.historyTypeName == "Labor overloadForm Form":
                historyFormToDelete = FormHistory.get(FormHistory.formHistoryID == form.formHistoryID)
                overloadFormToDelete = OverloadForm.get(OverloadForm.overloadFormID == form.overloadForm.overloadFormID)
                overloadFormToDelete.delete_instance()
                historyFormToDelete.delete_instance()
        message = "Your selected form for {0} {1} has been withdrawn.".format(student.studentSupervisee.FIRST_NAME, student.studentSupervisee.LAST_NAME)
        flash(message, "success")
        return jsonify({"Success":True, "url":"/"})
    except Exception as e:
        print(e)
        message = "An error occured. Your selected form for {0} {1} was not withdrawn.".format(student.studentSupervisee.FIRST_NAME, student.studentSupervisee.LAST_NAME)
        flash(message, "danger")
        return jsonify({"Success": False, "url":"/"})
