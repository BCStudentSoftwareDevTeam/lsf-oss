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
from app.logic.buttonStatus import ButtonStatus
from app.models.supervisor import Supervisor
from app.logic.tracy import Tracy

@main_bp.route('/laborHistory/<id>', methods=['GET'])
def laborhistory(id):
    try:
        currentUser = require_login()
        if not currentUser:                    # Not logged in
            return render_template('errors/403.html')
        if not currentUser.isLaborAdmin:
            departmentsList = None
            if currentUser.Student and not currentUser.Supervisor:
                if currentUser.Student.ID != id:
                    return redirect('/laborHistory/' + currentUser.Student.ID)
            elif currentUser.Supervisor and not currentUser.Student:
                authorizedUser, departmentsList = laborHistoryAuthorizeUser(id, currentUser, currentUser.Supervisor.ID)
                if authorizedUser == False:
                    return render_template('errors/403.html', currentUser = currentUser), 403
        else:
            departmentsList = []
        student = Student.get(Student.ID == id)
        studentUser = User.get(User.Student == student)
        studentForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == student).order_by(LaborStatusForm.startDate.desc())
        formHistoryList = ""
        for form in studentForms:
            formHistoryList = formHistoryList + str(form.laborStatusFormID) + ","
        formHistoryList = formHistoryList[0:-1]
        return render_template( 'main/formHistory.html',
    				            title=('Labor History'),
                                student = student,
                                username=currentUser.username,
                                studentForms = studentForms,
                                formHistoryList = formHistoryList,
                                departmentsList = departmentsList,
                                currentUser = currentUser,
                                studentUserName = studentUser.username
                              )
    except Exception as e:
        print("Error Loading Student Labor History", e)
        return render_template('errors/500.html', currentUser = currentUser), 500

@main_bp.route("/laborHistory/download" , methods=['POST'])
def downloadFormHistory():
    """
    This function is called when the download button is pressed.  It runs a function for writing to an excel sheet that is in download.py.
    This function downloads the created excel sheet of the history from the page.
    """
    currentUser = require_login()
    try:
        data = request.form
        historyList = data["listOfForms"].split(',')
        excel = ExcelMaker()
        completePath = excel.makeExcelStudentHistory(historyList)
        filename = completePath.split('/').pop()
        return send_file(completePath, mimetype='text/csv', as_attachment=True, attachment_filename=filename)
    except:
        return render_template('errors/500.html', currentUser = currentUser), 500

@main_bp.route('/laborHistory/modal/<statusKey>', methods=['GET'])
def populateModal(statusKey):
    """
    This function creates the modal and populates it with the history of a selected position.  It works with the openModal() function in laborhistory.js
    to create the modal, and append all of the data gathered here form the database to the modal.  It also sets a button state which decides which buttons
    to put on the modal depending on what form is in the history.
    """
    try:
        currentUser = require_login()
        if not currentUser:                    # Not logged in
            return render_template('errors/403.html', currentUser = currentUser), 403
        forms = FormHistory.select().where(FormHistory.formID == statusKey).order_by(FormHistory.createdDate.desc(), FormHistory.formHistoryID.desc())
        statusForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == statusKey)
        student = User.get(User.Student == statusForm[0].studentSupervisee)
        currentDate = datetime.date.today()
        pendingformType = None
        buttonState = None
        for form in forms:
            if form.modifiedForm != None:  # If a form has been adjusted then we want to retrieve supervisors names using the new and old values stored in modified table
                if form.modifiedForm.fieldModified == "Supervisor": # if supervisor field in adjust forms has been modified,
                    newSupervisorID = form.modifiedForm.newValue    # use the supervisor pidm in the field modified to find supervisor in User table.
                    newSupervisor = Supervisor.get(Supervisor.PIDM == newSupervisorID)
                    # we are temporarily storing the supervisor name in new value,
                    # because we want to show the supervisor name in the hmtl template.
                    form.modifiedForm.oldValue = form.formID.supervisor.FIRST_NAME + " " + form.formID.supervisor.LAST_NAME # old supervisor name
                    form.modifiedForm.newValue = newSupervisor.FIRST_NAME +" "+ newSupervisor.LAST_NAME
                if form.modifiedForm.fieldModified == "Position": # if position field has been modified in adjust form then retriev position name.
                    newPositionCode = form.modifiedForm.newValue
                    newPosition = Tracy().getPositionFromCode(newPositionCode)
                    # temporarily storing the new position name in new value, and old position name in old value
                    # because we want to show these information in the hmtl template.
                    form.modifiedForm.newValue = newPosition.POSN_TITLE + " (" + newPosition.WLS+")"
                    form.modifiedForm.oldValue = form.formID.POSN_TITLE + " (" + form.formID.WLS+")"
        for form in forms:
            if currentUser.Student and currentUser.username == student.username:
                buttonState = ButtonStatus.show_student_labor_eval_button
                break
            elif currentUser.Supervisor.ID != (form.createdBy.Supervisor.ID or form.formID.supervisor.ID):
                buttonState = ButtonStatus.no_buttons # otherwise, show the notification
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
                if form.modifiedForm != None:
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
