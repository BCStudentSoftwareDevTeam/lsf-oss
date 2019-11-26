from app.controllers.main_routes import *
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *
from flask import json, jsonify

@main_bp.route('/studentOverloadApp/<formId>', methods=['GET', 'POST'])
# @login_required
def studentOverloadApp(formId):
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    print(1)
    overloadForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formId)
    prefillStudentName = overloadForm.studentSupervisee.FIRST_NAME + " "+ overloadForm.studentSupervisee.LAST_NAME
    prefillStudentBnum = overloadForm.studentSupervisee.ID
    prefillStudentCPO = overloadForm.studentSupervisee.STU_CPO
    prefillStudentClass = overloadForm.studentSupervisee.CLASS_LEVEL
    prefillTerm = overloadForm.termCode.termName
    prefillDepartment = overloadForm.department.DEPT_NAME
    prefillPosition = overloadForm.POSN_TITLE
    prefillHoursOverload = overloadForm.weeklyHours
    listOfTerms = []
    today = date.today()
    todayYear = today.year
    termYear = todayYear * 100
    studentSpecificLabor = LaborStatusForm.select(LaborStatusForm.laborStatusFormID).where(LaborStatusForm.studentSupervisee_id == prefillStudentBnum,
                                                                                           LaborStatusForm.jobType == "Primary",
                                                                                           LaborStatusForm.termCode.between(termYear-1, termYear + 15))
    formIDList = []
    for i in studentSpecificLabor:
        print (getattr(i, "laborStatusFormID"),"ids")
        studentSpecificHistory = FormHistory.select().where((FormHistory.formID == i) & ((FormHistory.status == "Approved") | (FormHistory.status == "Approved Reluctantly")))
        print(studentSpecificHistory)
        currentPrimary = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == i)
        formIDList.append(currentPrimary)
    print(currentPrimary)

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
                            currentPrimary = formIDList
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
