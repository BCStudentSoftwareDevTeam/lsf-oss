from app.controllers.main_routes import *
from app.models.user import *
from app.login_manager import require_login

@main_bp.route('/studentOverloadApp', methods=['GET', 'POST'])
# @login_required
def studentOverloadApp():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    return render_template( 'main/studentOverloadApp.html',
				            title=('student Overload Application'),
                            username = current_user
                          )
