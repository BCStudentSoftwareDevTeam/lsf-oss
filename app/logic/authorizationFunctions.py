from app.models.laborStatusForm import *
from app.models.formHistory import *
from app.models.status import *


def laborHistoryAuthorizeUser(id, UserID):
    """
    If the current user is not an admin, then we can only allow them to see the labor history of a
    given BNumber if the BNumber is tied to a labor status form that is tied to a department where the
    current user is a supervisor or created a labor status form for the department
    """
    try:
        authorizedUser = False
        status = Status.get(Status.statusName == "Approved")
        allStudentDepartments = LaborStatusForm.select(LaborStatusForm.department).where(LaborStatusForm.studentSupervisee == id).distinct()
        allUserDepartments = FormHistory.select(FormHistory.formID.department).join_from(FormHistory, LaborStatusForm).where((FormHistory.formID.supervisor == UserID) | (FormHistory.createdBy == UserID)).distinct()
        for userDepartment in allUserDepartments:
            for studentDepartment in allStudentDepartments:
                if userDepartment.formID.department == studentDepartment.department:
                    authorizedUser = True
                    break
        departmentsList = []
        for i in allUserDepartments:
            departmentsList.append(i.formID.department.departmentID)
        return(authorizedUser, departmentsList)
    except Exception as e:
        print('Error authorizing user to access students labor history', type(e).__name__, e)
