from app.controllers.main_routes import *
from app.models.user import *
from app.login_manager import require_login

@main_bp.route('/modifyPending', methods=['GET', 'POST'])
# @login_required
def modifyPending():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    return render_template( 'main/modifyPending.html',
				            title=('Modify Pending'),
                            username = current_user
                          )
