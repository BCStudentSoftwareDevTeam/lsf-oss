from app.controllers.admin_routes import admin
from app.login_manager import require_login
from flask import render_template
# from app.controllers.admin_routes.allPendingForms import x, y, z
# from app.controllers.main_routes.laborHistory import x, y, z

@admin_route('/admin/generalSearch', methods=['GET'])
def generalSearch():
    currentUser = require_login()
    if not currentUser or not currentUser.isLaborAdmin:
        return render_template('errors/403.html'), 403

    return render_template('admin/allPendingForms.html',
                            title = "General Search")
