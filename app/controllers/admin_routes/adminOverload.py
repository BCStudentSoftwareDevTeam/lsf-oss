from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.login_manager import require_login

@admin.route('/adminOverload', methods=['GET', 'POST'])
# @login_required
def adminOverload():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    users = User.select()
    return render_template( 'admin/adminOverload.html',
				            title=('Admin Overload'),
                            username = current_user,
                            users = users
                          )
