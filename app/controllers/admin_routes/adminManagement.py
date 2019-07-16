from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin


@admin.route('/adminManagement', methods=['GET', 'POST'])
# @login_required
def admin_Management():
    username = load_user('heggens')
    users = User.select()
    firstname = User.select()
    lastname = User.select()
    return render_template( 'admin/adminManagement.html',
				            title=('Admin Management'),
                            username = username,
                            users = users,
                            firstname = firstname,
                            lastname = lastname
                          )
