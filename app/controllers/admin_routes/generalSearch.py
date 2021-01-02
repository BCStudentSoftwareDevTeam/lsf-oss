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
# from app.controllers.admin_routes.allPendingForms import x, y, z
# from app.controllers.main_routes.laborHistory import x, y, z

@admin.route('/admin/generalSearch', methods=['GET', 'POST'])
def generalSearch():
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

    queryResult = request.form['data']
    queryDict = json.loads(queryResult)

    draw = int(request.form['draw'])
    start = int(request.form['start'])
    length = int(request.form['length'])
    sortColIndex = int(request.form["order[0][column]"])
    order = request.form['order[0][dir]']
    print("col-----", sortColIndex, order)
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

    expression = reduce(operator.and_, clauses) # TODO: add a comment to say what this does

    query = (FormHistory.select().join(LaborStatusForm, on=(FormHistory.formID == LaborStatusForm.laborStatusFormID))
                        .join(Department, on=(LaborStatusForm.department == Department.departmentID))
                        .join(Supervisor, on=(LaborStatusForm.supervisor == Supervisor.ID))
                        .join(Student, on=(LaborStatusForm.studentSupervisee == Student.ID))
                        .join(Term, on=(LaborStatusForm.termCode == Term.termCode))
                        .where(expression))

    recordsTotal = query.count()
    if order == "desc":
        filteredQuery = query.order_by(-colIndexColNameMap[sortColIndex]).limit(length).offset(start)
    elif order == "asc":
        filteredQuery = query.order_by(colIndexColNameMap[sortColIndex]).limit(length).offset(start)

    data = []
    for form in filteredQuery:
        record = []
        record.append(form.formID.termCode.termName)
        record.append(form.formID.department.DEPT_NAME)
        record.append(form.formID.supervisor.FIRST_NAME + " " + form.formID.supervisor.LAST_NAME)
        record.append(form.formID.studentSupervisee.FIRST_NAME + " " + form.formID.studentSupervisee.LAST_NAME)
        record.append(form.formID.POSN_CODE + " (" + form.formID.WLS + ")")
        record.append(form.formID.weeklyHours)
        record.append(form.formID.startDate.strftime('%m/%d/%y') + " - " + form.formID.endDate.strftime('%m/%d/%y'))
        record.append(form.createdBy.username)
        record.append("")
        data.append(record)

    formsDict = {"draw": draw, "recordsTotal": recordsTotal, "recordsFiltered": recordsTotal, "data": data}

    return jsonify(formsDict)
