from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
#from app.models.manageDepartments import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import*

@admin.route('/admin/manageDepartments', methods=['GET', 'POST'])
# @login_required
def manage_departments():
    username = load_user('heggens')
    users = User.select()
    return render_template( 'admin/manageDepartments.html')
    title=('Manage Departments')
