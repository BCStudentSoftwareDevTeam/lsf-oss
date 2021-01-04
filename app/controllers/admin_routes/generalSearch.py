from app.controllers.admin_routes import admin
from app.login_manager import require_login
from flask import render_template, request, json, jsonify, redirect, url_for
from app.models.term import Term
from app.models.department import Department
from app.models.supervisor import Supervisor
from app.models.student import Student
from app.models.laborStatusForm import LaborStatusForm
from app.models.formHistory import FormHistory
from app.models.historyType import HistoryType
from app.models.status import Status
import operator
from functools import reduce

@admin.route('/admin/generalSearch', methods=['GET', 'POST'])
def generalSearch():
    '''
    When the request is GET the function populates the General Search interface dropdown menus with their corresponding values.
    If the request is POST it also populates the datatable with data.
    '''
    currentUser = require_login()
    if not currentUser or not currentUser.isLaborAdmin:
        return render_template('errors/403.html'), 403

    terms = Term.select()
    departments = Department.select()
    supervisors = Supervisor.select()
    students = Student.select()

    if request.method == 'POST':
        return getDatatableData(request)

    return render_template('admin/generalSearch.html',
                            title = "General Search",
                            terms = terms,
                            supervisors = supervisors,
                            students = students,
                            departments = departments,
                            )


def getDatatableData(request):
    '''
    This function runs a query based on selected options in the front-end and retrieves the appropriate forms.
    Then, it puts all the retrieved data in appropriate form to be send to the ajax call in the JS file.
    '''
    queryResult = request.form['data']
    queryDict = json.loads(queryResult)

    draw = int(request.form['draw'])
    start = int(request.form['start'])
    length = int(request.form['length'])
    sortColIndex = int(request.form["order[0][column]"])
    order = request.form['order[0][dir]']
    colIndexColNameMap = {  0: Term.termCode,
                            1: Department.DEPT_NAME,
                            2: FormHistory.formID.supervisor.FIRST_NAME,
                            3: Student.FIRST_NAME,
                            4: FormHistory.formID.POSN_CODE,
                            5: FormHistory.formID.weeklyHours,
                            6: FormHistory.formID.startDate,
                            7: FormHistory.createdBy}

    termCode = queryDict.get('termCode', "")
    departmentId = queryDict.get('departmentID', "")
    supervisorId = queryDict.get('supervisorID', "")
    studentId = queryDict.get('studentID', "")
    formStatusList = queryDict.get('formStatus', "") # checkboxes
    formTypeList = queryDict.get('formType', "")

    fieldValueMap = { Term.termCode: termCode,
                     Department.departmentID: departmentId,
                     Student.ID: studentId,
                     Supervisor.ID: supervisorId,
                     FormHistory.status: formStatusList,
                     FormHistory.historyType: formTypeList}
    clauses = []
    for field, value in fieldValueMap.items():
        if value != "" and value:
            # "is" is used to compare the two peewee objects.
            if field is FormHistory.historyType:
                for val in value:
                    clauses.append(field == val)
            elif field is FormHistory.status:
                for val in value:
                    clauses.append(field == val)
            else:
                clauses.append(field == value)

    expression = reduce(operator.and_, clauses) # This expression created AND statements using model fields and selec picker values

    query = (FormHistory.select().join(LaborStatusForm, on=(FormHistory.formID == LaborStatusForm.laborStatusFormID))
                        .join(Department, on=(LaborStatusForm.department == Department.departmentID))
                        .join(Supervisor, on=(LaborStatusForm.supervisor == Supervisor.ID))
                        .join(Student, on=(LaborStatusForm.studentSupervisee == Student.ID))
                        .join(Term, on=(LaborStatusForm.termCode == Term.termCode))
                        .where(expression))

    # Sorting Functionality of the datatable
    recordsTotal = query.count()
    if order == "desc":
        filteredQuery = query.order_by(-colIndexColNameMap[sortColIndex]).limit(length).offset(start)
    elif order == "asc":
        filteredQuery = query.order_by(colIndexColNameMap[sortColIndex]).limit(length).offset(start)

    # Putting the data in the correct format to be used by the JS file
    supervisorStudentHTML = '<a href="#" class="hover_indicator" aria-label="{}">{} </a><a href="mailto:{}"><span class="glyphicon glyphicon-envelope mailtoIcon"></span></a>'
    departmentHTML = '<a href="#" class="hover_indicator" aria-label="{}-{}"> {}</a>'
    positionHTML = '<a href="#" class="hover_indicator" aria-label="{}"> {}</a><br>{}'
    data = []
    for form in filteredQuery:
        record = []
        record.append(form.formID.termCode.termName)
        record.append(departmentHTML.format(
              form.formID.department.ORG,
              form.formID.department.ACCOUNT,
              form.formID.department.DEPT_NAME))

        currentSupervisor = supervisorStudentHTML.format(
                            form.formID.supervisor.ID,
                            ' '.join([form.formID.supervisor.FIRST_NAME, form.formID.supervisor.LAST_NAME]),
                            form.formID.supervisor.EMAIL)

        if form.adjustedForm.fieldAdjusted == "supervisor":
            supervisor = supervisorStudentHTML.format(form.adjustedForm.oldValue.ID, form.adjustedForm.newValue, form.adjustedForm.oldValue.email)

        record.append(currentSupervisor)

        record.append(supervisorStudentHTML.format(
              form.formID.studentSupervisee.ID,
              ' '.join([form.formID.studentSupervisee.FIRST_NAME,
              form.formID.studentSupervisee.LAST_NAME]),
              form.formID.studentSupervisee.STU_EMAIL))

        record.append(positionHTML.format(
              form.formID.POSN_TITLE,
              form.formID.POSN_CODE + " (" + form.formID.WLS + ")",
              form.formID.jobType))

        hours = form.formID.weeklyHours if form.formID.weeklyHours else form.formID.contractHours
        record.append(hours)

        record.append("<br>".join([form.formID.startDate.strftime('%m/%d/%y'),
                      form.formID.endDate.strftime('%m/%d/%y')]))

        record.append(supervisorStudentHTML.format(
              form.createdBy.supervisor.ID,
              form.createdBy.username,
              form.createdBy.supervisor.EMAIL,
              form.createdDate.strftime('%m/%d/%y')))

        laborHistoryId = form.formHistoryID
        laborStatusFormId = form.formID.laborStatusFormID
        actionsButton = getActionButtonLogic(form, laborHistoryId, laborStatusFormId)

        record.append(actionsButton)
        data.append(record)

    formsDict = {"draw": draw, "recordsTotal": recordsTotal, "recordsFiltered": recordsTotal, "data": data}

    return jsonify(formsDict)

def getActionButtonLogic(form, laborHistoryId, laborStatusFormId):
    '''
    This function determines the options shown on the Actions dropdown, which depends on form type and form status.
    '''

    actionsButtonDropdownHTML = '<div class="dropdown"><button class="btn btn-primary dropdown-toggle" type="button" id="menu1" data-toggle="dropdown">Actions</button>' +\
                                '<ul class="dropdown-menu" role="menu" aria-labelledby="menu1" style="min-width: 100%;">{}{}{}{}</ul></div>'
    actionsListHTML = '<li role="presentation"><a role="menuitem" href="{}">{}</a></li>'
    manageOptionHTML = actionsListHTML.format('#', '<span id="{}" onclick="{}">Manage</span>')
    denyApproveOptionsHTML = actionsListHTML.format('#', '<span id="{}" onclick="{}" data-toggle="modal" data-target="#{}">{}</span>')
    modifyOptionHTML = actionsListHTML.format('/alterLSF/{lsfID}', '<span id="edit_{lsfID}">Modify</span>')

    # Actions button and its options
    actionsButton = ""
    approve = ""
    deny = ""
    manage = ""
    modify = ""

    if form.historyType.historyTypeName == "Labor Status Form":
        manage = manageOptionHTML.format(laborHistoryId, f"loadLaborHistoryModal({laborHistoryId})")
        actionsButton = actionsButtonDropdownHTML.format(manage, approve, deny, modify)

    if form.status.statusName == "Pending":
        if form.overloadForm:
            manage = manageOptionHTML.format(laborHistoryId, f"loadOverloadModal({laborHistoryId}, {laborStatusFormId})")
        elif form.releaseForm:
            manage = manageOptionHTML.format(laborHistoryId, f"loadReleaseModal({laborHistoryId}, {laborStatusFormId})")
        elif form.adjustedForm:
            deny = denyApproveOptionsHTML.format(f"reject_{laborHistoryId}", f"insertDenial({laborHistoryId})", 'denyModal', 'Deny')
            approve = denyApproveOptionsHTML.format("", f"insertApprovals({laborHistoryId})", 'approvalModal', 'Approve')
        else:
            modify = modifyOptionHTML.format(lsfID = laborStatusFormId)
            deny = denyApproveOptionsHTML.format(f"reject_{laborHistoryId}", f"insertDenial({laborHistoryId})", 'denyModal', 'Deny')
            approve = denyApproveOptionsHTML.format("", f"insertApprovals({laborHistoryId});", 'approvalModal', 'Approve')
        actionsButton = actionsButtonDropdownHTML.format(manage, approve, deny, modify)

    return actionsButton
