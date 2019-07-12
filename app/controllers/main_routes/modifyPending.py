from app.controllers.main_routes import *
from app.models.user import *

@main_bp.route('/modifyPending', methods=['GET', 'POST'])
# @login_required
def modifyPending():
    username = load_user('heggens')
    return render_template( 'main/modifyPending.html',
				            title=('Modify Pending'),
                            username = username
                          )
