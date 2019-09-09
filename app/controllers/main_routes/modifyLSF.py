from app.controllers.main_routes import *
from app.models.user import *
from flask_bootstrap import bootstrap_find_resource
from app.login_manager import require_login


@main_bp.route('/modifyLSF', methods=['GET', 'POST'])
# @login_required
def modifyLSF():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    return render_template( 'main/modifyLSF.html',
				            title=('Modify LSF'),
                            username = current_user
                          )
