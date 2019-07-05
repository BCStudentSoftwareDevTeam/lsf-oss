from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.term import *
from flask_bootstrap import bootstrap_find_resource

@main_bp.route('/laborstatusform', methods=['GET', 'POST'])
# @login_required
def laborStatusForm():

    username = load_user('heggens')  #FIXME Hardcoding users is bad
    forms = LaborStatusForm.select()
    students = User.select()        #FIXME not all students, but it's names for now
    terms = Term.select().where(Term.active == True)
    return render_template( 'main/laborstatusform.html',
				            title=('Labor Status Form'),
                            username = username,
                            forms = forms,
                            students = students,
                            terms = terms
                          )
