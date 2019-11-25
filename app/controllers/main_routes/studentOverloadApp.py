from app.controllers.main_routes import *
from app.models.user import *
from app.login_manager import require_login
from app.models.laborStatusForm import *
from datetime import date
from app.models.formHistory import *

@main_bp.route('/studentOverloadApp/<formId>', methods=['GET', 'POST'])
# @login_required
def studentOverloadApp(formId):
    current_user = require_login()
    if not current_user:        # Not logged in
        return render_template('errors/403.html')
    print(1)
    overloadForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == formId)
    prefillStudentName = overloadForm.studentSupervisee.FIRST_NAME + " "+ overloadForm.studentSupervisee.LAST_NAME
    prefillStudentBnum = overloadForm.studentSupervisee.ID
    prefillStudentCPO = overloadForm.studentSupervisee.STU_CPO
    prefillStudentClass = overloadForm.studentSupervisee.CLASS_LEVEL
    prefillTerm = overloadForm.termCode.termName
    prefillDepartment = overloadForm.department.DEPT_NAME
    prefillPosition = overloadForm.POSN_TITLE
    prefillHoursOverload = overloadForm.weeklyHours
    listOfTerms = []
    today = date.today()
    todayYear = today.year
    termYear = todayYear * 100
    currentAcademicTerm = Term.select().where(Term.termCode.between(termYear-1, termYear + 15))
    print(2)
    for term in currentAcademicTerm:
        listOfTerms.append(term)
    print(3)
    print(listOfTerms)
    studentSpecificLabor = LaborStatusForm.select(LaborStatusForm.laborStatusFormID).where(LaborStatusForm.studentSupervisee_id == prefillStudentBnum, LaborStatusForm.jobType == "Primary")
    print(4)
    for i in studentSpecificLabor:
        print(i, "Im here")
    print(5)
    studentSpecificHistory = FormHistory.select().where((FormHistory.formID == '%s' %i) for i in studentSpecificLabor)
    studentHistory = studentSpecificHistory.where(
                            ((studentSpecificHistory.status_id == "Approved") | (studentSpecificHistory.status == "Approved Reluctantly"))
    ).get()
    print(studentHistory)

    return render_template( 'main/studentOverloadApp.html',
				            title=('student Overload Application'),
                            username = current_user,
                            overloadForm = overloadForm,
                            prefillStudentName = prefillStudentName,
                            prefillStudentBnum = prefillStudentBnum,
                            prefillStudentCPO = prefillStudentCPO,
                            prefillStudentClass = prefillStudentClass,
                            prefillTerm = prefillTerm,
                            prefillDepartment = prefillDepartment,
                            prefillPosition = prefillPosition,
                            prefillHoursOverload = prefillHoursOverload
                          )
