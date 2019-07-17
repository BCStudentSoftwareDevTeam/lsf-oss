from app.controllers.admin_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.controllers.admin_routes import admin
from app.controllers.errors_routes.handlers import *

@admin.route('/admin', methods=['GET', 'POST'])
def admin_tables():
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')
        if not current_user.isLaborAdmin:       # Not an admin
            return render_template('errors/403.html')

        # Logged in & Admin
        users = User.select()
        return render_template( 'admin/adminTables.html',
                                title=('Admin'),
                                username=current_user.username,
                                users=users
                                )
    except:
        render_template('errors/500.html')
