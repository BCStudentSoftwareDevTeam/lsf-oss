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


@main_bp.route('/modifyLSF/<laborStatusKey>', methods=['GET', 'POST']) #History modal called it laborStatusKey
# @login_required
def modifyLSF(laborStatusKey):
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    #If logged in....
    #Step 1: get form attached to the student (via labor history modal)
    form = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
    #Step 2: get prefill data from said form, then the data that populates dropdowns for supervisors and position
    prefillstudent = form.studentSupervisee.FIRST_NAME + " "+ form.studentSupervisee.LAST_NAME+" ("+form.studentSupervisee.ID+")"###FIXME (ALL OF THESE): query to students previous lsf form to pull specific fields.
    prefillsupervisor = form.supervisor.FIRST_NAME +" "+ form.supervisor.LAST_NAME
    prefilldepartment = form.department.DEPT_NAME
    prefillposition = form.POSN_TITLE #FIXME: add WLS to this; they should be connected
    prefilljobtype = form.jobType
    prefillterm = form.termCode.termName
    if form.weeklyHours != None:
        prefillhours = form.weeklyHours
        print ("WeeklyHours",prefillhours)
    else:
        prefillhours = form.contractHours
        print ("ContractHours",prefillhours)
    prefillnotes = form.supervisorNotes
    #These are the data fields to populate our dropdowns(Supervisor. Position, WLS,)
    supervisors = STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc()) # modeled after LaborStatusForm.py
    positions = STUPOSN.select(STUPOSN.POSN_CODE).distinct() #FIX ME: 1) needs to be specific to that department
                                                            # 2) have WLS displayed with it since they are connected (like LSF interface)
    wls = STUPOSN.select(STUPOSN.WLS).distinct()
    #Step 3: send data to front to populate html
    return render_template( 'main/modifyLSF.html',
				            title=('Modify LSF'),
                            username = current_user,
                            prefillstudent = prefillstudent,
                            prefillsupervisor = prefillsupervisor,
                            prefilldepartment = prefilldepartment,
                            prefillposition = prefillposition,
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
        #FIXME: I think this well be a separate save since its a separate dictionary for a separate table
        #old value
        #new value
        #date
    except:
        flash("An error has occurred, your changes were NOT saved. Please try again.","error")
        return json.dumps({"error":0})
