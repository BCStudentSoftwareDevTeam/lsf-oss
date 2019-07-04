from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *

@main_bp.route('/laborstatusform', methods=['GET', 'POST'])
# @login_required
def laborStatusForm():
    username = load_user('heggens')  #FIXME Hardcoding users is bad
    forms = LaborStatusForm.select()
    return render_template( 'main/laborstatusform.html',
				            title=('Labor Status Form'),
                            username = username,
                            forms = forms
                          )
