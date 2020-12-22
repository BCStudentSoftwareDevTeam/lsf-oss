from app.controllers.admin_routes import admin
from app.login_manager import require_login
from flask import render_template
from app.models.term import Term
from app.models.department import Department
from app.models.student import Student
from app.models.supervisor import Supervisor
# from app.controllers.admin_routes.allPendingForms import x, y, z
# from app.controllers.main_routes.laborHistory import x, y, z

@admin.route('/admin/generalSearch', methods=['GET'])
def generalSearch():
    currentUser = require_login()
    if not currentUser or not currentUser.isLaborAdmin:
        return render_template('errors/403.html'), 403

    terms = Term.select().where(Term.termState == "open")
    departments = Department.select()
    supervisors = Supervisor.select()
    students = Student.select()
    # TODO: Write the main SEARCH query

    return render_template('admin/allPendingForms.html',
                            title = "General Search",
                            terms = terms,
                            supervisors = supervisors,
                            students = students,
                            departments = departments
                            )

# TODO: A new function to run the search query
