from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource
from app.models.Tracy.studata import *

@main_bp.route('/laborstatusform', methods=['GET', 'POST'])
# @login_required
def laborStatusForm():

    username = load_user('heggens')  #FIXME Hardcoding users is bad
    forms = LaborStatusForm.select()
    students = STUDATA.select()
    terms = Term.select().where(Term.termState == "open")#changed to term state, open, closed, inactive
    users = User.select()
    print(users)
    return render_template( 'main/laborStatusForm.html',
				            title=('Labor Status Form'),
                            username = username,#Passing of variables from controller to front
                            forms = forms,
                            students = students,
                            terms = terms,
                            users = users
                          )
