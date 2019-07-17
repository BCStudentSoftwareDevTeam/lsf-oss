from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin


@admin.route('/adminOverload', methods=['GET', 'POST'])
# @login_required
def adminOverload():
    username = load_user('heggens')
    users = User.select()
    return render_template( 'admin/adminOverload.html',
				            title=('Admin Overload'),
                            username = username,
                            users = users
                          )
