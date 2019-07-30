from app.controllers.main_routes import *
from app.controllers.main_routes.main_routes import *
from app.controllers.main_routes.laborHistory import *
from app.models.user import *
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.Tracy.stuposn import *
from flask_bootstrap import bootstrap_find_resource
from app.login_manager import require_login
from datetime import *


@main_bp.route('/modifyLSF', methods=['GET', 'POST']) #FIXME: ADD FORM ID TO URL(PASSED FROM LABOR HISTORY)
# @login_required
def modifyLSF():
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)
    #form = query to attach form to form id
    #Step 2: get data from said form ###FIXME ALL OF THESE: query to students previous lsf form to pull specific fields.
    prefillstudent = "Willy Wonka" #form.studentSupervisee
    prefillsupervisor = "Scott Heggen (sheggen)" #form.supervisor
    prefilldepartment = "Computer Science" #form.department
    prefillposition = "Janitor" #form.POSN_TITLE
    prefillwls = "WLS 1" #form.WLS
    prefilljobtype = "Primary" #form.jobType
    prefillterm = "AY 2019-2020" #form.termCode
    prefillhours = "0-5" #form.weeklyHours ##FIXME  Its not always weekly. sometimes its contract.
    prefillnotes = "Kids went missing in his factory... sketchy business...but he's alright i guess" #form.supervisorNotes
    #These are the data fields to populate our dropdowns(Supervisor. Position, WLS,)
    supervisors = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # modeled after LaborStatusForm.py
    positions = STUPOSN.select(STUPOSN.POSN_CODE).distinct() #FIX ME: needs to be specific to that department
    wls = STUPOSN.select(STUPOSN.WLS).distinct() #Shouldnt wls be tied to position...?? why are there 2 separate fields for it on our page then..?
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
                            prefillnotes = prefillnotes,
                            supervisors = supervisors,
                            positions = positions,
                            wls = wls
                          )

@main_bp.route("/saveChanges/<laborStatusFormID>", methods=["POST"]) #Should this be the reroute or should it be in JS?
def saveChanges(laborStatusFormID):
    #Takes dictionary from ajax and dumps to db
    try:
        laborstatusform = laborStatusForm.get(laborStatusForm.laborStatusFormID==laborStatusFormID)
        data = request.form
        laborstatusform.supervisor = (data['supervisor'])
        laborstatusform.POSN_TITLE = (data['position'])
        laborstatusform.WLS = (data['WLS'])
        laborstatusform.jobType = (data['jobType'])
        laborstatusform.weeklyHours = (data['weeklyHours']) #FIXME: not always weekly hours (if secondary/break).
        laborstatusform.laborSupervisorNotes = (data['laborSupervisorNotes'])
        #modifiedForm #Not sure if this will work...
        modifiedform = modifiedForm.get(modifiedForm.modifiedFormID==modifiedFormID)
        modifiedform.fieldModified = (data['fieldModified'])
        modifiedform.oldValue = (data['oldValue'])
        modifiedform.oldValue = (data['newValue'])
        modifiedform.effectiveDate = (data['effectiveDate'])
        #FIXME: dunno what's goin on with these rn....
        #field modified
        #old value
        #new value
    except:
        flash("An error has occurred, your changes were NOT saved. Please try again.","error")
        return json.dumps({"error":0})
