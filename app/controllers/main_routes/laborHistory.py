from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app, send_file
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
# from app.models.formHistory import FormHistory
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
from app.models.Tracy.stuposn import STUPOSN

@main_bp.route('/laborHistory/<id>', methods=['GET'])
def laborhistory(id):
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:
            # If the current user is not an admin, then we can only allow them to see the labor history of a
            # given BNumber if the BNumber is tied to a labor status form that is tied to a department where the
            # current user is a supervisor or created a labor status form for the department
            isLaborAdmin = False
            authorizedUser = False
            allStudentDepartments = LaborStatusForm.select(LaborStatusForm.department).where(LaborStatusForm.studentSupervisee == id).distinct()
            allUserDepartments = FormHistory.select(FormHistory.formID.department).join_from(FormHistory, LaborStatusForm).where((FormHistory.formID.supervisor == current_user.UserID) | (FormHistory.createdBy == current_user.UserID)).distinct()
            for userDepartment in allUserDepartments:
                for studentDepartment in allStudentDepartments:
                    if userDepartment.formID.department == studentDepartment.department:
                        authorizedUser = True
                        break
            if authorizedUser == False:
                return render_template('errors/403.html')
            departmentsList = []
            for i in allUserDepartments:
                departmentsList.append(i.formID.department.departmentID)
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

    Additionally, this function overrides the original information of a Labor Status Form that was adjusted and approved.
    """
    try:
        forms = FormHistory.select().where(FormHistory.formID == statusKey).order_by(FormHistory.createdDate.desc())
        statusForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == statusKey)
        LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == statusKey) # getting the specific labor status form that will be used for determining whether the form is adjusted and approved.
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
                        buttonState = 2 # Withdraw button and modify button
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
                            if currentDate > form.formID.termCode.adjustmentCutOff:
                                buttonState = 4 #Release and rehire buttons
                                break
                            else:
                                buttonState = 3 #Release, adjustment, and rehire buttons
                                break
                        elif currentDate > form.formID.termCode.termEnd:
                            buttonState = 0 #Only rehire
                            break
            overrideOriginalStatusFormOnAdjustmentFormApproval(form, LSF) # Function that overrides info if an adjusted form is approved.
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


def overrideOriginalStatusFormOnAdjustmentFormApproval(form, LSF):
    """
    This function checks whether an Adjustment Form is approved. If yes, it overrides the information
    in the original Labor Status Form with the new information coming from approved Adjustment Form.

    The only fields that will ever be modified in an adjustment form are: supervisor, position, and hours. 
    """
    if form.modifiedForm != None and form.status.statusName == "Approved":
        if form.modifiedForm.fieldModified == "supervisor":
            d, created = User.get_or_create(PIDM = form.modifiedForm.newValue)
            if not created:
                LSF.supervisor = d.UserID
            LSF.save()
            if created:
                tracyUser = STUSTAFF.get(STUSTAFF.PIDM == form.modifiedForm.newValue)
                tracyEmail = tracyUser.EMAIL
                tracyUsername = tracyEmail.find('@')
                user = User.get(User.PIDM == form.modifiedForm.newValue)
                user.username   = tracyEmail[:tracyUsername]
                user.FIRST_NAME = tracyUser.FIRST_NAME
                user.LAST_NAME  = tracyUser.LAST_NAME
                user.EMAIL      = tracyUser.EMAIL
                user.CPO        = tracyUser.CPO
                user.ORG        = tracyUser.ORG
                user.DEPT_NAME  = tracyUser.DEPT_NAME
                user.save()
                LSF.supervisor = d.PIDM
                LSF.save()
        if form.modifiedForm.fieldModified == "POSN_CODE":
            LSF.POSN_CODE = form.modifiedForm.newValue
            position = STUPOSN.get(STUPOSN.POSN_CODE == form.modifiedForm.newValue)
            LSF.POSN_TITLE = position.POSN_TITLE
            LSF.WLS = position.WLS
            LSF.save()
        if form.modifiedForm.fieldModified == "weeklyHours":
            allTermForms = LaborStatusForm.select().join_from(LaborStatusForm, Student).where((LaborStatusForm.termCode == LSF.termCode) & (LaborStatusForm.laborStatusFormID != LSF.laborStatusFormID) & (LaborStatusForm.studentSupervisee.ID == LSF.studentSupervisee.ID))
            totalHours = 0
            if allTermForms:
                for i in allTermForms:
                    totalHours += i.weeklyHours
            previousTotalHours = totalHours + int(form.modifiedForm.newValue)
            newTotalHours = totalHours + int(form.modifiedForm.newValue)
            if previousTotalHours <= 15 and newTotalHours > 15:
                newLaborOverloadForm = OverloadForm.create(studentOverloadReason = None)
                user = User.get(User.username == cfg["user"]["debug"])
                newFormHistory = FormHistory.create( formID = LSF.laborStatusFormID,
                                                    historyType = "Labor Overload Form",
                                                    createdBy = user.UserID,
                                                    overloadForm = newLaborOverloadForm.overloadFormID,
                                                    createdDate = date.today(),
                                                    status = "Pending")
             # emails are commented out for testing purposes
                # overloadEmail = emailHandler(newFormHistory.formHistoryID)
                # overloadEmail.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(newFormHistory.formHistoryID))
            LSF.weeklyHours = int(form.modifiedForm.newValue)
            LSF.save()

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
        return render_template('errors/500.html')
        return(jsonify({"Success": False}))


@main_bp.route('/laborHistory/modal/withdrawform', methods=['POST'])
def withdraw_form():
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
