from app.controllers.main_routes import *
from app.models.user import *
from flask_bootstrap import bootstrap_find_resource

@main_bp.route('/modifyLSF', methods=['GET', 'POST'])
# @login_required
def modifyLSF():
    username = load_user('heggens')
    return render_template( 'main/modifyLSF.html',
				            title=('Modify LSF'),
                            username = username
                          )
