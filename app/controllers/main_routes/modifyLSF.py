from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.user import *
from app.models.Tracy.studata import STUDATA
from flask_bootstrap import bootstrap_find_resource
from app.login_manager import require_login
from datetime import *



@main_bp.route('/modifyLSF', methods=['GET', 'POST'])
# @login_required
def modifyLSF():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)

    #Step 2: get data from said form
    prefillstudent = 1
    prefillsupervisor = 2
    prefilldepartment = 3
    prefillposition = 4
    prefillwls = 5
    prefilljobtype = 6
    prefillterm = 7
    prefillhours = 8
    current_time = datetime.now()
    prefilldateneeded = current_time.strftime('%m/%d/%Y')
    prefillnotes = 10

    #Step 3: send data to front to populate html
    return render_template( 'main/modifyLSF.html',
				            title=('Modify LSF'),
                            username = current_user,
                            prefillstudent = prefillstudent,
                            prefillsupervisor = prefillsupervisor,
                            prefilldepartment = prefilldepartment,
                            prefillposition = prefillposition,
                            prefillwls = prefillwls,
                            prefilljobtype = prefilljobtype,
                            prefillterm = prefillterm,
                            prefillhours = prefillhours,
                            prefilldateneeded = prefilldateneeded,
                            prefillnotes = prefillnotes
                          )
