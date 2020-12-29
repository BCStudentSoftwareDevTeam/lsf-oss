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
"""
queryResult:  {'draw': '1', 'columns[0][data]': 'Term', 'columns[0][name]': '', 'columns[0][searchable]': 'true', 'columns[0][orderable]': 'true', 'columns[0][search][value]': '', 'columns[0][search][regex]': 'false', 'columns[1][data]': 'Department', 'columns[1][name]': '', 'columns[1][searchable]': 'true', 'columns[1][orderable]': 'true', 'columns[1][search][value]': '', 'columns[1][search][regex]': 'false', 'columns[2][data]': 'Supervisor', 'columns[2][name]': '', 'columns[2][searchable]': 'true', 'columns[2][orderable]': 'true', 'columns[2][search][value]': '', 'columns[2][search][regex]': 'false', 'columns[3][data]': 'Students', 'columns[3][name]': '', 'columns[3][searchable]': 'true', 'columns[3][orderable]': 'true', 'columns[3][search][value]': '', 'columns[3][search][regex]': 'false', 'columns[4][data]': 'Position', 'columns[4][name]': '', 'columns[4][searchable]': 'true', 'columns[4][orderable]': 'true', 'columns[4][search][value]': '', 'columns[4][search][regex]': 'false', 'columns[5][data]': 'Hours', 'columns[5][name]': '', 'columns[5][searchable]': 'true', 'columns[5][orderable]': 'true', 'columns[5][search][value]': '', 'columns[5][search][regex]': 'false', 'columns[6][data]': 'Contract Dates', 'columns[6][name]': '', 'columns[6][searchable]': 'true', 'columns[6][orderable]': 'true', 'columns[6][search][value]': '', 'columns[6][search][regex]': 'false', 'columns[7][data]': 'Created', 'columns[7][name]': '', 'columns[7][searchable]': 'true', 'columns[7][orderable]': 'true', 'columns[7][search][value]': '', 'columns[7][search][regex]': 'false', 'columns[8][data]': '', 'columns[8][name]': '', 'columns[8][searchable]': 'true', 'columns[8][orderable]': 'true', 'columns[8][search][value]': '', 'columns[8][search][regex]': 'false', 'order[0][column]': '0', 'order[0][dir]': 'asc', 'start': '0', 'length': '10', 'search[value]': '', 'search[regex]': 'false'}

"""
@admin.route('/admin/generalSearch', methods=['GET', 'POST'])
# @admin.route('/admin/generalSearch/<queryResult>', methods=['POST', 'GET'])
def generalSearch():

    currentUser = require_login()
    if not currentUser or not currentUser.isLaborAdmin:
        return render_template('errors/403.html'), 403

    terms = Term.select()
    departments = Department.select()
    supervisors = Supervisor.select()
    students = Student.select()

    # query = None  # TODO: write if statements in JavaScript to handle the NoneType case
    if request.method == 'POST':
        # queryResult = (request.data).decode("utf-8")  # This turns byte data into a string\
        queryResult = dict(request.form);
        print("queryResult: ", queryResult)
        # queryDict = json.loads(queryResult)
        # termCode = request.form['term']
        # departmentId = request.form['department']
        # supervisorId = request.form['supervisor']
        # studentId = request.form['student']
        # formStatusList = request.form.getlist('formStatus') # checkboxes
        # formTypeList = request.form.getlist('formType')
        print("here--------")
        fieldValueMap = { Term.termCode: queryResult['term'],
                         Department.departmentID: queryResult['department'],
                         Student.ID: queryResult['student'],
                         Supervisor.ID: queryResult['supervisor']}

        clauses = []
        for field, value in fieldValueMap.items():
            if value:
                # "is" is used to compare the two peewee objects.
                if field is FormHistory.historyType:
                    for val in value:
                        clauses.append(field == val)
                elif field is FormHistory.status:
                    for val in value:
                        clauses.append(field == val)
                else:
                    clauses.append(field == value)

        expression = reduce(operator.and_, clauses)

        query = (FormHistory.select().join(LaborStatusForm, on=(FormHistory.formID == LaborStatusForm.laborStatusFormID))
                            .join(Department, on=(LaborStatusForm.department == Department.departmentID))
                            .join(Supervisor, on=(LaborStatusForm.supervisor == Supervisor.ID))
                            .join(Student, on=(LaborStatusForm.studentSupervisee == Student.ID))
                            .join(Term, on=(LaborStatusForm.termCode == Term.termCode))
                            .where(expression))
        print("Almost there!!!")

        data = []
        for form in query:
            record = []
            record.append(form.formID.termCode.termName)
            record.append(form.formID.department.DEPT_NAME)
            record.append(form.formID.supervisor.FIRST_NAME + " " + form.formID.supervisor.LAST_NAME)
            record.append(form.formID.studentSupervisee.FIRST_NAME + " " + form.formID.studentSupervisee.LAST_NAME)
            record.append(form.formID.POSN_CODE + " (" + form.formID.WLS + ")")
            record.append(form.formID.weeklyHours)
            record.append(form.formID.startDate.strftime('%m/%d/%y') + " - " + form.formID.endDate.strftime('%m/%d/%y'))
            record.append(form.createdBy.username)

            data.append(record)

        formsDict = {"draw": 1, "recordsTotal": query.count(), "recordsFiltered": query.count(), "data": data}
        # print("formsDict: ", formsDict)
        # print("data: ", data)
        return jsonify(formsDict)
        # return jsonify(formsDict)
        # queryResult = (request.data).decode("utf-8")  # This turns byte data into a string
        # queryDict = json.loads(queryResult)
        # termCode = request.form['term']
        # departmentId = request.form['department']
        # supervisorId = request.form['supervisor']
        # studentId = request.form['student']
        # formStatusList = request.form.getlist('formStatus') # checkboxes
        # formTypeList = request.form.getlist('formType')
        #
        # fieldValueMap = { Term.termCode: termCode,
        #                  Department.departmentID: departmentId,
        #                  Student.ID: studentId,
        #                  Supervisor.ID: supervisorId,
        #                  FormHistory.historyType: formTypeList,
        #                  FormHistory.status: formStatusList }
        #
        # clauses = []
        # for field, value in fieldValueMap.items():
        #     if value:
        #         # "is" is used to compare the two peewee objects.
        #         if field is FormHistory.historyType:
        #             for val in value:
        #                 clauses.append(field == val)
        #         elif field is FormHistory.status:
        #             for val in value:
        #                 clauses.append(field == val)
        #         else:
        #             clauses.append(field == value)
        #
        # expression = reduce(operator.and_, clauses)
        #
        # query = (FormHistory.select().join(LaborStatusForm, on=(FormHistory.formID == LaborStatusForm.laborStatusFormID))
        #                     .join(Department, on=(LaborStatusForm.department == Department.departmentID))
        #                     .join(Supervisor, on=(LaborStatusForm.supervisor == Supervisor.ID))
        #                     .join(Student, on=(LaborStatusForm.studentSupervisee == Student.ID))
        #                     .join(Term, on=(LaborStatusForm.termCode == Term.termCode))
        #                     .where(expression))
        # print("Almost there!!!")
        #
        # return render_template('admin/generalSearch.html',
        #                         title = "General Search",
        #                         terms = terms,
        #                         supervisors = supervisors,
        #                         students = students,
        #                         departments = departments,
        #                         formList = query
        #                         )
    # print("queryResult in GET: ", queryResult)
    return render_template('admin/generalSearch.html',
                            title = "General Search",
                            terms = terms,
                            supervisors = supervisors,
                            students = students,
                            departments = departments,
                            )

# @admin.route('/admin/queryResult', methods=['POST'])
# def generalSearchQuery():
    # queryResult = request.data # This turns byte data into a string
    # queryDict = json.loads(queryResult)
    #
    # fieldValueMap = { Term.termCode: queryDict['termCode'],
    #          Department.departmentID: queryDict['departmentID'],
    #          Student.ID: queryDict['studentID'],
    #          Supervisor.ID: queryDict['supervisorID'],
    #          FormHistory.historyType: queryDict['formType'],
    #          FormHistory.status: queryDict['formStatus'] }
    #
    # clauses = []
    # for field, value in fieldValueMap.items():
    #     if value:
    #         # "is" is used to compare the two peewee objects.
    #         if field is FormHistory.historyType:
    #             for val in value:
    #                 clauses.append(field == val)
    #         elif field is FormHistory.status:
    #             for val in value:
    #                 clauses.append(field == val)
    #         else:
    #             clauses.append(field == value)
    #
    # expression = reduce(operator.and_, clauses)
    #
    # query = (FormHistory.select().join(LaborStatusForm, on=(FormHistory.formID == LaborStatusForm.laborStatusFormID))
    #                     .join(Department, on=(LaborStatusForm.department == Department.departmentID))
    #                     .join(Supervisor, on=(LaborStatusForm.supervisor == Supervisor.ID))
    #                     .join(Student, on=(LaborStatusForm.studentSupervisee == Student.ID))
    #                     .join(Term, on=(LaborStatusForm.termCode == Term.termCode))
    #                     .where(expression))
    # print("Almost there!!!")
    #
    # data = []
    # for form in query:
    #     record = []
    #     record.append(form.formID.termCode.termName)
    #     record.append(form.formID.department.DEPT_NAME)
    #     record.append(form.formID.supervisor.FIRST_NAME + " " + form.formID.supervisor.LAST_NAME)
    #     record.append(form.formID.studentSupervisee.FIRST_NAME + " " + form.formID.studentSupervisee.LAST_NAME)
    #     record.append(form.formID.POSN_CODE + " (" + form.formID.WLS + ")")
    #     record.append(form.formID.weeklyHours)
    #     record.append(form.formID.startDate.strftime('%m/%d/%y') + " - " + form.formID.endDate.strftime('%m/%d/%y'))
    #     record.append(form.createdBy.username)
    #
    #     data.append(record)
    #
    # formsDict = {"draw": 1, "recordsTotal": query.count(), "recordsFiltered": query.count(), "data": data}
    # print("formsDict: ", formsDict)
    # print("data: ", data)
    # return jsonify(formsDict)
