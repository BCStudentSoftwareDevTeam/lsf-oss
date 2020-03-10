from app.controllers.admin_routes import admin
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *
from flask import json, jsonify
from flask import request, render_template
from app.models.overloadForm import *

@admin.route('/admin/financialAidOverloadApproval/<overloadKey>', methods=['GET']) # the form ID here is the ID from overloadForm table
def financialAidOverload(overloadKey):
    '''
    This function prefills all the information for a student's current job and overload request
    '''
    current_user = require_login()

    if not current_user:                    # Not logged in
        return render_template('errors/403.html')
    if not (current_user.isFinancialAidAdmin or current_user.isSaasAdmin):       # Not an admin
        return render_template('errors/403.html')



    overload = FormHistory.get(FormHistory.overloadForm == overloadKey)
    print("overload form", overload)

    lsfForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == overload.formID)
    print("lsf form",lsfForm.laborStatusFormID)

    totalCurrentHours = FormHistory.get(FormHistory.formID == lsfForm, overload.status == "Approved", lsfForm.jobType == "Primary")
    # when the status is approved it shows that the form do not exist. Which makes studentSecondaryLabor
    # rThe column on weekly hours is confusing, I think we need to create an extra column for overload hours separate
    # how do I tell which labor status form id in the form history table was for Primary?


    getoverloadReason = OverloadForm.get(OverloadForm.overloadFormID == overload.formID)
    print("this is overload reason: ", getoverloadReason)
    # the following lines prefills the information for student
    studentName = lsfForm.studentSupervisee.FIRST_NAME + " "+ lsfForm.studentSupervisee.LAST_NAME
    studentBnum = lsfForm.studentSupervisee.ID
    department = lsfForm.department.DEPT_NAME
    position = lsfForm.POSN_TITLE
    supervisor = lsfForm.supervisor.FIRST_NAME +" "+ lsfForm.supervisor.LAST_NAME
    overloadHours = lsfForm.weeklyHours
    overloadReason = getoverloadReason.overloadReason
    print("here", overloadReason)
    totalCurrentHours = totalCurrentHours.weeklyHours
    laborOfficeNotes=lsfForm.laborDepartmentNotes
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
    currentHours = 0
    for i in formIDPrimary:
        for j in i:
            if str(j.status) != "Pending":
                currentHours += j.formID.weeklyHours
    for i in formIDSecondary:
        for j in i:
            if str(j.status) != "Pending":
                currentHours += j.formID.weeklyHours
    totalFormHours = currentHours + overloadHours
    print ("total form hours", totalFormHours)


# will need to add term to the interface and then have a prefill variable
    return render_template( 'admin/financialAidOverload.html',
                        username = current_user,
                        overload = overload,
                        studentName = studentName,
                        studentBnum = studentBnum,
                        department = department,
                        position = position,
                        supervisor= supervisor,
                        currentPrimary = formIDPrimary,
                        currentSecondary = formIDSecondary,
                        totalCurrentHours = totalCurrentHours,
                        totalFormHours = totalFormHours,
                        overloadReason = overloadReason,
                        laborOfficeNotes = laborOfficeNotes
                      )
