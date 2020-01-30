from app.controllers.admin_routes import admin
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *
from flask import json, jsonify
from flask import request, render_template
from app.models.overloadForm import *

@admin.route('/admin/financialAidOverloadApproval/<overloadFormID>', methods=['GET']) # the form ID here is the ID from overloadForm table
def financialAidOverload(overloadFormID):
    current_user = require_login()

    if not current_user:                    # Not logged in
        return render_template('errors/403.html')
    if not (current_user.isFinancialAidAdmin or current_user.isSaasAdmin):       # Not an admin
        return render_template('errors/403.html')

    overloadForm = FormHistory.get(FormHistory.formHistoryID == overloadFormID)
    lsfForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == overloadForm.formID)
    # the following lines prefills the information for student
    studentName = lsfForm.studentSupervisee.FIRST_NAME + " "+ lsfForm.studentSupervisee.LAST_NAME
    studentBnum = lsfForm.studentSupervisee.ID
    department = lsfForm.department.DEPT_NAME
    position = lsfForm.POSN_TITLE
    overloadHours= lsfForm.weeklyHours
    today = date.today()
    termYear = today.year
    termCodeYear = Term.select(Term.termCode).where(Term.termCode.between(termYear-1, termYear + 15))
    currentTerm = str(lsfForm.termCode.termCode)[-2:]
    TermsNeeded=[]

    for term in termCodeYear:
        if str(term)[-2:] == "11" or str(term)[-2:] == "12" or str(term)[-2:]== "00":
            TermsNeeded.append(term)

    studentPrimaryLabor = LaborStatusForm.select(LaborStatusForm.laborStatusFormID).where(LaborStatusForm.studentSupervisee_id == studentBnum,
                                                                                           LaborStatusForm.jobType == "Primary",
                                                                                           LaborStatusForm.termCode.in_(TermsNeeded))

    studentSecondaryLabor = LaborStatusForm.select(LaborStatusForm.laborStatusFormID).where(LaborStatusForm.studentSupervisee_id == studentBnum,
                                                                                               LaborStatusForm.jobType == "Secondary",
                                                                                               LaborStatusForm.termCode.in_(TermsNeeded))
    formIDPrimary = []
    for i in studentPrimaryLabor:
        studentPrimaryHistory = FormHistory.select().where((FormHistory.formID == i) & (FormHistory.historyType == "Labor Status Form") & ((FormHistory.status == "Approved") | (FormHistory.status == "Approved Reluctantly") | (FormHistory.status == "Pending")))
        formIDPrimary.append(studentPrimaryHistory)
    formIDSecondary = []
    for i in studentSecondaryLabor:
        studentSecondaryHistory = FormHistory.select().where((FormHistory.formID == i) & (FormHistory.historyType == "Labor Status Form") & ((FormHistory.status == "Approved") | (FormHistory.status == "Approved Reluctantly") | (FormHistory.status == "Pending")))
        formIDSecondary.append(studentSecondaryHistory)
    totalCurrentHours = 0
    for i in formIDPrimary:
        for j in i:
            if str(j.status) != "Pending":
                totalCurrentHours += j.formID.weeklyHours
    for i in formIDSecondary:
        for j in i:
            if str(j.status) != "Pending":
                totalCurrentHours += j.formID.weeklyHours
    totalFormHours = totalCurrentHours + overloadHours



# will need to add term to the interface and then have a prefill variable
    return render_template( 'admin/financialAidOverload.html',
                        username = current_user,
                        overloadForm = overloadForm,
                        studentName = studentName,
                        studentBnum = studentBnum,
                        department = department,
                        position = position,
                        overloadHours = overloadHours,
                        currentPrimary = formIDPrimary,
                        currentSecondary = formIDSecondary,
                        totalCurrentHours = totalCurrentHours,
                        totalFormHours = totalFormHours
                      )
