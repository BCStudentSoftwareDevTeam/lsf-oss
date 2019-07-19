from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborReleaseForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *
from app.models.department import *
from app.models.user import *
from app.controllers.errors_routes.handlers import *
from app.login_manager import require_login


@main_bp.route('/laborReleaseForm', methods=['GET', 'POST'])
# @login_required
def laborReleaseForm():

    current_user = require_login()
    if not current_user:
        render_template("errors/403.html")
    if not current_user.isLaborAdmin:
        render_template("errors/403.html")

    students = STUDATA.select()
    department = Department.select()
    users = User.select()
    laborReleaseform = LaborReleaseForm.select()

    return render_template( 'main/laborReleaseForm.html',
				            title=('Labor Release Form'),
                            students = students,
                            department = department,
                            users = users,
                            laborReleaseForm = laborReleaseForm
                          )
