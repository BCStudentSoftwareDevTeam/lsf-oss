from app.controllers.admin_routes import admin
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *
from flask import json, jsonify
from flask import request, render_template
from app.models.overloadForm import *
from app import cfg

@admin.route('/admin/financialAidOverloadApproval/<overloadKey>', methods=['GET']) # we get the form ID when FinancialAid or SAAS clicks on the link they receive via email.
def financialAidOverload(overloadKey):
    '''
    This function prefills all the information for a student's current job and overload request.
    '''
    current_user = require_login() #we need to check to see if the person logged in is SAAS or FinancialAid #TODO

    if not current_user: # Not logged in
        return render_template('errors/403.html')
    if not (current_user.isFinancialAidAdmin or current_user.isSaasAdmin): # Not an admin
        return render_template('errors/403.html')

    overloadForm = FormHistory.get(FormHistory.overloadForm == overloadKey) # get access to overload form
    lsfForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == overloadForm.formID) # get the labor status form that is tied to the overload form

    primaryHours = {}
    ###-------- Popoulate Current Position -------###
    # Get all labor status forms for the same student in the same term and see if they have a primary position.
    # IF YES: populate the "Current Position" Fields with the information from that labor status form.
    allLaborStatusForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == lsfForm.studentSupervisee.ID, LaborStatusForm.termCode == lsfForm.termCode.termCode)
    statusList = ["Approved", "Approved Reluctantly", "Pending"]
    for form in allLaborStatusForms:
        if form.jobType == "Primary":
            statusHistory = FormHistory.get(FormHistory.formID == form.laborStatusFormID) # prepopulate only and only if primary labor status form is not denied
            if statusHistory.status.statusName in statusList:
                studentName = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME
                studentBnum = form.studentSupervisee.ID
                position = form.POSN_TITLE
                supervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
                department = form.department.DEPT_NAME
                primaryPositionHours = form.weeklyHours
                primaryHours["primaryHours"] = primaryPositionHours

    ###-------- Popoulate Overload Request Information -------###
    # Get the overload form submitted for the student. Then, populate the Overload Request Information section with the data from overload form.
    overloadPosition = lsfForm.POSN_TITLE
    totalOverloadHours = lsfForm.weeklyHours + primaryHours["primaryHours"]
    studentOverloadReason = overloadForm.overloadForm.overloadReason
    laborOfficeNotes = lsfForm.laborDepartmentNotes
    today = date.today()
    termYear = today.year
    termCodeYear = Term.select(Term.termCode).where(Term.termCode.between(termYear-1, termYear + 15))
    currentTerm = str(lsfForm.termCode.termCode)[-2:]
    contractDate = "{} - {}".format(lsfForm.startDate.strftime('%m/%d/%y'), lsfForm.endDate.strftime('%m/%d/%y'))

## TODO: Check to see if primary + secondary hours gets summed up.

# will need to add term to the interface and then have a prefill variable
    return render_template( 'admin/financialAidOverload.html',
                        username = current_user,
                        overload = overloadForm,
                        studentName = studentName,
                        studentBnum = studentBnum,
                        department = department,
                        position = position,
                        supervisor= supervisor,
                        primaryPositionHours = primaryPositionHours,
                        studentOverloadReason = studentOverloadReason,
                        laborOfficeNotes = laborOfficeNotes,
                        contractDate = contractDate,
                        overloadPosition = overloadPosition,
                        totalOverloadHours = totalOverloadHours
                      )

@admin.route("/admin/financialAidOverloadApproval/<status>", methods=["POST"])
def formDenial(status):
    ''' This fucntion will get the status (Approved/Denied) and make the appropriate
    changes in the database for that specific overload form'''
    print(status)
    if status == "denial":
        newStatus = "Denied"
    elif status == "approval":
        newStatus = "Approved"
    else:
        return jsonify({'error': 'Unknown Status'}), 500
    try:
        # Here we need to change the db with the appropriate information
        createdUser = User.get(username = cfg['user']['debug'])
        rsp = eval(request.data.decode("utf-8"))
        print(rsp, "dictionary")
        return jsonify({'success':True}), 200
    except Exception as e:
        print("Unable to Deny the OverloadForm",type(e).__name__ + ":", e)
        return jsonify({'error': "Unable to Deny the form"}), 500
