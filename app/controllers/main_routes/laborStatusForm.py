from flask_login import login_required

from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
# from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *

@main_bp.route('/laborstatusform', methods=['GET', 'POST'])
def laborStatusForm():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    # Logged in
    forms = LaborStatusForm.select()
    students = STUDATA.select()
    terms = Term.select().where(Term.termState == "open")#changed to term state, open, closed, inactive
    return render_template( 'main/laborstatusform.html',
                            title=('Labor Status Form'),
                            username=current_user,#Passing of variables from controller to front
                            forms=forms,
                            students=students,
                            terms=terms
                          )
