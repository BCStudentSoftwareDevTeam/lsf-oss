from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborReleaseForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *

@main_bp.route('/laborReleaseForm', methods=['GET', 'POST'])
# @login_required
def laborReleaseForm():

    username = load_user('heggens')  #FIXME Hardcoding users is bad
    return render_template( 'main/laborReleaseForm.html',
				            title=('Labor Release Form'),
                            username = username
                          )
