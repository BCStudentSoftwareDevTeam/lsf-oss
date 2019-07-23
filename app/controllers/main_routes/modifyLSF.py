from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.user import *
from app.models.Tracy.studata import STUDATA
from flask_bootstrap import bootstrap_find_resource
from app.login_manager import require_login
from datetime import *


@main_bp.route('/modifyLSF', methods=['GET', 'POST']) #FIXME: ADD FORM ID TO URL
# @login_required
def modifyLSF():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)

    #Step 2: get data from said form
    #FIX ALL OF THESE
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
    prefillnotes = "Include your notes about your modification here."
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

@main_bp.route("/saveChanges/<laborStatusFormID>", methods=["POST"])
def saveChanges(laborStatusFormID):
    #Takes dictionary from ajax and dumps to db
    try:
        laborstatusform = laborStatusForm.get(laborStatusForm.laborStatusFormID==laborStatusFormID)
        data = request.form
        laborstatusform.primarySupervisor = (data['primarySupervisor']) #FIXME: not always primarySupervisor
        laborstatusform.position = (data['position'])
        laborstatusform.WLS = (data['WLS'])
        laborstatusform.jobType = (data['jobType'])
        laborstatusform.weeklyHours = (data['weeklyHours']) #FIXME: not always weekly hours (if secondary)
        ####Effective date should go to formhistory/modified form...
        laborstatusform.laborSupervisorNotes = (data['laborSupervisorNotes'])
        #modifiedForm
        modifiedform = modifiedForm.get(modifiedForm.modifiedFormID==modifiedFormID)
        modifiedform.effectiveDate = (data['effectiveDate'])
        #FIXME: dunno what's goin on with these rn....
        #field modified
        #old value
        #new value
    except:
        flash("An error has occurred, your changes were NOT saved. Please try again.","error")
        return json.dumps({"error":0})
