from app.controllers.main_routes import *
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *
from flask import json, jsonify
from flask import request
from app.models.overloadForm import *

@main_bp.route('/studentOverloadApp/<formId>', methods=['GET', 'POST']) # the form ID here is the ID from formHistory table
# @login_required
def studentOverloadApp(formId):
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    overloadForm = FormHistory.get(FormHistory.formHistoryID == formId)

    lsfForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == overloadForm.formID)
    prefillStudentName = lsfForm.studentSupervisee.FIRST_NAME + " "+ lsfForm.studentSupervisee.LAST_NAME
    prefillStudentBnum = lsfForm.studentSupervisee.ID
    prefillStudentCPO = lsfForm.studentSupervisee.STU_CPO
    prefillStudentClass = lsfForm.studentSupervisee.CLASS_LEVEL
    prefillTerm = lsfForm.termCode.termName
    prefillDepartment = lsfForm.department.DEPT_NAME
    prefillPosition = lsfForm.POSN_TITLE
    prefillHoursOverload = lsfForm.weeklyHours
    listOfTerms = []
    today = date.today()
    todayYear = today.year
    termYear = todayYear * 100
    termCodeYear = Term.select(Term.termCode).where(Term.termCode.between(termYear-1, termYear + 15))
    currentTerm = str(lsfForm.termCode.termCode)[-2:]
    TermsNeeded=[]
    for term in termCodeYear:
        if str(term)[-2:] == currentTerm or str(term)[-2:]== "00":
            TermsNeeded.append(term)
    print(TermsNeeded,"terms needed")

    studentSecondaryLabor = LaborStatusForm.select(LaborStatusForm.laborStatusFormID).where(LaborStatusForm.studentSupervisee_id == prefillStudentBnum,
                                                                                               LaborStatusForm.jobType == "Secondary",
                                                                                               LaborStatusForm.termCode.in_(TermsNeeded))

    studentPrimaryLabor = LaborStatusForm.select(LaborStatusForm.laborStatusFormID).where(LaborStatusForm.studentSupervisee_id == prefillStudentBnum,
                                                                                           LaborStatusForm.jobType == "Primary",
                                                                                           LaborStatusForm.termCode.in_(TermsNeeded))
    print(studentPrimaryLabor ,"student primary labor")
    formIDPrimary = []
    for i in studentPrimaryLabor:
        studentPrimaryHistory = FormHistory.select().where((FormHistory.formID == i) & ((FormHistory.status == "Approved") | (FormHistory.status == "Approved Reluctantly") | (FormHistory.status == "Pending")))
        print(studentPrimaryHistory, "form History")
        formIDPrimary.append(studentPrimaryHistory)
    print(formIDPrimary, "the end result")
    formIDSecondary = []
    print(studentSecondaryLabor ,"student secondary labor")
    for i in studentSecondaryLabor:
        studentSecondaryHistory = FormHistory.select().where((FormHistory.formID == i) & ((FormHistory.status == "Approved") | (FormHistory.status == "Approved Reluctantly") | (FormHistory.status == "Pending")))
        print(studentSecondaryHistory, "form History")
        formIDSecondary.append(studentSecondaryHistory)
    print(formIDSecondary, "the end result")
    totalCurrentHours = 0
    for i in formIDPrimary:
        for j in i:
            if str(j.status) != "Pending":
                totalCurrentHours += j.formID.weeklyHours
    print(totalCurrentHours)
    for i in formIDSecondary:
        for j in i:
            if str(j.status) != "Pending":
                totalCurrentHours += j.formID.weeklyHours
    print(totalCurrentHours)
    return render_template( 'main/studentOverloadApp.html',
				            title=('student Overload Application'),
                            username = current_user,
                            overloadForm = overloadForm,
                            prefillStudentName = prefillStudentName,
                            prefillStudentBnum = prefillStudentBnum,
                            prefillStudentCPO = prefillStudentCPO,
                            prefillStudentClass = prefillStudentClass,
                            prefillTerm = prefillTerm,
                            prefillDepartment = prefillDepartment,
                            prefillPosition = prefillPosition,
                            prefillHoursOverload = prefillHoursOverload,
                            currentPrimary = formIDPrimary,
                            currentSecondary = formIDSecondary,
                            totalCurrentHours = totalCurrentHours
                          )

@main_bp.route("/studentOverloadApp/getPrimary/<formID>", methods=['GET'])
def getPrimaryHours(formID):
    """ Get the hour for the selected primary position """
    print(formID)
    Hours = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formID)
    HourDict = {}
    HourDict[Hours.laborStatusFormID] = {"primaryHour": Hours.weeklyHours}
    print(HourDict)
    return json.dumps(HourDict)

@main_bp.route("/studentOverloadApp/getSecondary/<formID>", methods=['GET'])
def getSecondaryHours(formID):
    """ Get the hour for the selected secondary position """
    print(formID)
    Hours = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formID)
    HourDict = {}
    HourDict[Hours.laborStatusFormID] = {"secondaryHour": Hours.weeklyHours}
    print(HourDict)
    return json.dumps(HourDict)

@main_bp.route('/studentOverloadApp/update', methods=['POST'])
def updateDatabase():
    try:
        # NEED TO ADD CURRENT PRIMARY AND CURRENT SECONDARY AFTER THE MIGRATION
        rsp = eval(request.data.decode("utf-8"))
        if rsp:
            formId = rsp.keys()
            for data in rsp.values():
                print(data)
                overloadform = OverloadForm.create(overloadReason = data["Notes"])
        return jsonify({"Success": True})
    except Exception as e:
        print("ERROR: " + str(e))
        return jsonify({"Success": False})
