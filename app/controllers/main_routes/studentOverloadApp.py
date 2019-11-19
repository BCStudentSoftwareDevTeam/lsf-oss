from app.controllers.main_routes import *
from app.models.user import *
from app.login_manager import require_login

@main_bp.route('/studentOverloadApp/<formId>', methods=['GET', 'POST'])
# @login_required
def studentOverloadApp(formId):
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')

    overloadForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formId)
    prefillStudentName = overloadForm.studentSupervisee.FIRST_NAME + " "+ overloadForm.studentSupervisee.LAST_NAME
    prefillStudentBnum = overloadForm.studentSupervisee.ID
    prefillStudentCPO = overloadForm.studentSupervisee.STU_CPO
    prefillStudentClass = overloadForm.studentSupervisee.CLASS_LEVEL
    prefillStudentPrimaryPos = overloadForm.studentSupervisee.LAST_POSN
    prefillTerm = overloadForm.termCode.termName
    prefillDepartment = overloadForm.department.DEPT_NAME
    prefillPosition = overloadForm.POSN_TITLE
    prefillHoursOverload = overloadForm.weeklyHours


    return render_template( 'main/studentOverloadApp.html',
				            title=('student Overload Application'),
                            username = current_user,
                            overloadForm = overloadForm,
                            prefillStudentName = prefillStudentName,
                            prefillStudentBnum = prefillStudentBnum,
                            prefillStudentCPO = prefillStudentCPO,
                            prefillStudentClass = prefillStudentClass,
                            prefillStudentPrimaryPos = prefillStudentPrimaryPos,
                            prefillTerm = prefillTerm,
                            prefillDepartment = prefillDepartment,
                            prefillPosition = prefillPosition,
                            prefillHoursOverload = prefillHoursOverload
                          )
