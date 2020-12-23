from app.controllers.admin_routes import admin
from app.login_manager import require_login
from flask import render_template, request, json, jsonify
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

    query = None  # TODO: write if statements in JavaScript to handle the NoneType case
    if request.method == 'POST':
        queryResult = (request.data).decode("utf-8")  # This turns byte data into a string
        queryDict = json.loads(queryResult)

        fieldValueMap = { Term.termCode: queryDict['termCode'],
                 Department.departmentID: queryDict['departmentID'],
                 Student.ID: queryDict['studentID'],
                 Supervisor.ID: queryDict['supervisorID'],
                 FormHistory.historyType: queryDict['formType'],
                 FormHistory.status: queryDict['formStatus'] }

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

    terms = Term.select()
    departments = Department.select()
    supervisors = Supervisor.select()
    students = Student.select()

    return render_template('admin/allPendingForms.html',
                            title = "General Search",
                            terms = terms,
                            supervisors = supervisors,
                            students = students,
                            departments = departments,
                            formList = query
                            )

# # TODO: A new function to run the search query
# @admin.route('/admin/generalSearch/queryResult', methods=['POST'])
# def generalSearchQuery():
#     queryResult = (request.data).decode("utf-8")  # This turns byte data into a string
#     queryDict = json.loads(queryResult)
#
#     fieldValueMap = { Term.termCode: queryDict['termCode'],
#              Department.departmentID: queryDict['departmentID'],
#              Student.ID: queryDict['studentID'],
#              Supervisor.ID: queryDict['supervisorID'],
#              FormHistory.historyType: queryDict['formType'],
#              FormHistory.status: queryDict['formStatus'] }
#
#     clauses = []
#     for field, value in fieldValueMap.items():
#         if value:
#             # "is" is used to compare the two peewee objects.
#             if field is FormHistory.historyType:
#                 for val in value:
#                     clauses.append(field == val)
#             elif field is FormHistory.status:
#                 for val in value:
#                     clauses.append(field == val)
#             else:
#                 clauses.append(field == value)
#
#     expression = reduce(operator.and_, clauses)
#
#     query = (FormHistory.select().join(LaborStatusForm, on=(FormHistory.formID == LaborStatusForm.laborStatusFormID))
#                         .join(Department, on=(LaborStatusForm.department == Department.departmentID))
#                         .join(Supervisor, on=(LaborStatusForm.supervisor == Supervisor.ID))
#                         .join(Student, on=(LaborStatusForm.studentSupervisee == Student.ID))
#                         .join(Term, on=(LaborStatusForm.termCode == Term.termCode))
#                         .where(expression))
#     print("Almost there!!!")
#     return render_template('admin/allPendingForms.html',
#                             formList=query)
