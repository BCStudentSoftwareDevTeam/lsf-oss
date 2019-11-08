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
from fpdf import FPDF

@main_bp.route('/laborHistory/<id>', methods=['GET'])
def laborhistory(id):
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')

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
                                formHistoryList = formHistoryList
                              )
    except:
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

@main_bp.route("/laborHistory/pdf", methods=['POST'])
def downloadPDF():
    try:
        print("PDF");
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
        pdf.output("simple_demo.pdf")

        return "done"
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
                        if currentDate <= form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire button
                            break
                        elif currentDate > form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire
                            break
                    elif form.status.statusName == "Pending":
                        buttonState = None # no buttons
                        break
                    elif form.status.statusName == "Denied":
                        if currentDate <= form.formID.termCode.termEnd:
                            buttonState = 3   #Release, modify, and rehire buttons
                            break
                        elif currentDate > form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire
                            break
                if form.overloadForm != None:
                    if form.status.statusName == "Pending":
                        buttonState = 1 #Only withdraw button
                        break
                    if form.status.statusName == "Denied":
                        if currentDate <= form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire button
                            break
                        elif currentDate > form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire
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
                        if currentDate <= form.formID.termCode.termEnd:
                            buttonState = 0 #Rehire button
                            break
                        elif currentDate > form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire
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
        # print(e)
        return render_template('errors/500.html')
        return (jsonify({"Success": False}))

@main_bp.route('/laborHistory/modal/updatestatus', methods=['POST'])
def updatestatus_post():
    """
    This function deletes forms from the database when they are pending and the "withdraw" button is clicked.
    """
    try:
        rsp = eval(request.data.decode("utf-8"))
        student = LaborStatusForm.get(rsp["FormID"]).studentSupervisee.ID
        selectedPendingForms = FormHistory.select().join(Status).where(FormHistory.formID == rsp["FormID"]).where(FormHistory.status.statusName == "Pending").order_by(FormHistory.historyType.asc())
        for form in selectedPendingForms:
            try:
                OverloadForm.get(OverloadForm.overloadFormID == form.overloadForm.overloadFormID).delete_instance()
                form.delete_instance()
            except:
                pass
            try:
                ModifiedForm.get(ModifiedForm.modifiedFormID == form.modifiedForm.modifiedFormID).delete_instance()
                form.delete_instance()
            except:
                pass
            try:
                if form.historyType.historyTypeName == "Labor Status Form":
                    formID = form.formID.laborStatusFormID
                    form.delete_instance()
                    LaborStatusForm.get(formID).delete_instance()
            except:
                pass
        flash("Your selected form has been withdrawn.", "success")
        return jsonify({"Success":True, "url":"/laborHistory/" + student})
    except Exception as e:
        # print(e)
        return jsonify({"Success": False})
