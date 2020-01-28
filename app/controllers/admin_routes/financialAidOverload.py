from app.controllers.admin_routes import admin
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *
from flask import json, jsonify
from flask import request, render_template
from app.models.overloadForm import *

@admin.route('/admin/financialAidOverloadApproval/<overloadFormID>')
def financialAidOverload(overloadFormID):
    return render_template('admin/financialAidOverload.html')


    # studentPrimaryLabor = LaborStatusForm.select(LaborStatusForm.laborStatusFormID).where(LaborStatusForm.studentSupervisee_id == prefillStudentBnum,
    #                                                                                        LaborStatusForm.jobType == "Primary",
    #                                                                                        LaborStatusForm.termCode.in_(TermsNeeded))
    # formIDPrimary = []
    # for i in studentPrimaryLabor:
    #     studentPrimaryHistory = FormHistory.select().where((FormHistory.formID == i) & (FormHistory.historyType == "Labor Status Form") & ((FormHistory.status == "Approved") | (FormHistory.status == "Approved Reluctantly") | (FormHistory.status == "Pending")))
    #     formIDPrimary.append(studentPrimaryHistory)
    # formIDSecondary = []
    # for i in studentSecondaryLabor:
    #     studentSecondaryHistory = FormHistory.select().where((FormHistory.formID == i) & (FormHistory.historyType == "Labor Status Form") & ((FormHistory.status == "Approved") | (FormHistory.status == "Approved Reluctantly") | (FormHistory.status == "Pending")))
    #     formIDSecondary.append(studentSecondaryHistory)
    # totalCurrentHours = 0
    # for i in formIDPrimary:
    #     for j in i:
    #         if str(j.status) != "Pending":
    #             totalCurrentHours += j.formID.weeklyHours
    # for i in formIDSecondary:
    #     for j in i:
    #         if str(j.status) != "Pending":
    #             totalCurrentHours += j.formID.weeklyHours
    # totalFormHours = totalCurrentHours + prefillHoursOverload
    # return render_template( 'main/studentOverloadApp.html',
	# 			            title=('student Overload Application'),
    #                         username = current_user,
    #                         overloadForm = overloadForm,
    #                         prefillStudentName = prefillStudentName,
    #                         prefillStudentBnum = prefillStudentBnum,
    #                         prefillStudentCPO = prefillStudentCPO,
    # #                         prefillStudentClass = prefillStudentClass,
    #                         prefillTerm = prefillTerm,
    #                         prefillDepartment = prefillDepartment,
    #                         prefillPosition = prefillPosition,
    #                         prefillHoursOverload = prefillHoursOverload,
    #                         currentPrimary = formIDPrimary,
    #                         currentSecondary = formIDSecondary,
    #                         totalCurrentHours = totalCurrentHours,
    #                         totalFormHours = totalFormHours
    #                       )
#
# @main_bp.route('/studentOverloadApp/update', methods=['POST'])
# def updateDatabase():
#     try:
#         # NEED TO ADD CURRENT PRIMARY AND CURRENT SECONDARY AFTER THE MIGRATION
#         rsp = eval(request.data.decode("utf-8"))
#         if rsp:
#             formId = rsp.keys()
#             for data in rsp.values():
#                 overloadForm = OverloadForm.create(overloadReason = data["Notes"])
#                 formHistoryForm = FormHistory.get(FormHistory.formHistoryID == data["formID"])
#                 formHistoryForm.overloadForm = overloadForm.overloadFormID
#                 formHistoryForm.save()
#         return jsonify({"Success": True})
#     except Exception as e:
#         print("ERROR: " + str(e))
#         return jsonify({"Success": False})
