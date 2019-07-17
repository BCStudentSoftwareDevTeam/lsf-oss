from app.controllers.main_routes import *
from app.models.user import *

@main_bp.route('/studentOverloadApp', methods=['GET', 'POST'])
# @login_required
def studentOverloadApp():
    username = load_user('heggens')
    return render_template( 'main/studentOverloadApp.html',
				            title=('student Overload Application'),
                            username = username
                          )
