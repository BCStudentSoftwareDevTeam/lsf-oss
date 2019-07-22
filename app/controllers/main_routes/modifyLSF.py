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
@main_bp.route('/modifyLSF/getPrefills', methods=['GET'])
def getPrefills():
    #Function that pulls info/data from form history that user clicked to populate modify forms
    #Step 1: get form attached to the student
    # thestudent = LaborStatusForm.select(LaborStatusForm.studentSupervisee).where(LaborStatusForm.)#query to find student associated with form
    # theform = #query to find specific form they clicked from (from all student's forms)
    #Step 2: get data from said forms

    #Step 3: send data to front to populate html

    return render_template( '/modifyLSF/getPrefills',)
