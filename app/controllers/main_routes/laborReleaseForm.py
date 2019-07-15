from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborReleaseForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *
from app.models.department import *

@main_bp.route('/laborReleaseForm', methods=['GET', 'POST'])
# @login_required
def laborReleaseForm():

    username = load_user('heggens')  #FIXME Hardcoding users is bad
    students = STUDATA.select()
    department = Department.select()
    users = User.select()

    return render_template( 'main/laborReleaseForm.html',
				            title=('Labor Release Form'),
                            username = username,
                            students = students,
                            department = department,
                            users = users
                          )
