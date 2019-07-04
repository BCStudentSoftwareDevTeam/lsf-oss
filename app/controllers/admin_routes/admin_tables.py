from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin


@admin.route('/admin', methods=['GET', 'POST'])
# @login_required
def admin_tables():
    username = load_user('heggens')
    users = User.select()
    return render_template( 'admin/adminTables.html',
				            title=('Admin'),
                            username = username,
                            users = users
                          )
