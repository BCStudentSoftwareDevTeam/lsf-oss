from app.controllers.admin_routes import admin
from app.login_manager import require_login
from flask import render_template
from app.models.term import Term
from app.models.department import Department
from app.models.supervisor import Supervisor
from app.models.student import Student
from app.models.laborStatusForm import LaborStatusForm
from app.models.formHistory import FormHistory
import operator
# from app.controllers.admin_routes.allPendingForms import x, y, z
# from app.controllers.main_routes.laborHistory import x, y, z

@admin.route('/admin/generalSearch', methods=['GET'])
def generalSearch():
    currentUser = require_login()
    if not currentUser or not currentUser.isLaborAdmin:
        return render_template('errors/403.html'), 403

    terms = Term.select()
    departments = Department.select()
    supervisors = Supervisor.select()
    students = Student.select()

    return render_template('admin/allPendingForms.html',
                            title = "General Search",
                            terms = terms,
                            supervisors = supervisors,
                            students = students,
                            departments = departments
                            )

# TODO: A new function to run the search query
@admin.route('/admin/generalSearch/<queryJson>', methods=['GET'])
def generalSearchQuery(queryJson):
    ''' query = {   term: Fall 2020,
                    supervisor: Scott Heggen,
                    student: Hila Manalai,
                    department: CS,
                    formType: {pending: False, approved: True, denied: False},
                    formStatus: {adjusted: False, ...}

    SELECT * FROM formhistory
    JOIN laborstatusform ON laborstatusform.laborStatusFormID = formhistory.formID_id
    JOIN department ON laborstatusform.department_id = department.departmentID
    JOIN supervisor ON laborstatusform.supervisor_id = supervisor.ID
    JOIN student ON laborstatusform.studentSupervisee_id = student.ID
    JOIN term ON laborstatusform.termCode_id = term.termCode

    WHERE department.departmentID = 0
    AND supervisor.ID = 0
    AND student.ID = 0
    AND term.termCode = 201511;

    '''

    clauses = []
    for key, value in queryJson.items():
        if value:    # assuming value will be None if it is not selected by the user
            clauses.append(key == value)

    expression = reduce(operator.and_, clauses)

    query = (FormHistory.select().join(LaborStatusForm on=(LaborStatusForm.laborStatusFormID == FormHistory.formID))
                        .join(Department on=(LaborStatusForm.department == Department.departmentID))
                        .join(Supervisor on=(LaborStatusForm.supervisor == Supervisor.ID))
                        .join(Student on=(LaborStatusForm.student == Student.ID))
                        .join(Term on=(LaborStatusForm.termCode == Term.termCode))
                        .where(expression)
