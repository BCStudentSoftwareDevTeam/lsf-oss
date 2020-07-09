from app.models.laborStatusForm import *
from app.models.formHistory import *
from app.models.status import *


def authorizeUser_findAllDepartments(id, UserID, supervisorID=None):
    """
    If the current user is not an admin, and they are a supervisor,
    then we can only allow them to see the labor history of a
    given BNumber if the BNumber is tied to a labor status form that is tied to a department where the
    current user is a supervisor or created a labor status form for the department.
    OR when the current user is a student, then we allow them to see all forms
    in all departments that they are tied to.
    """
    try:
        departmentsList = []
        allStudentDepartments = LaborStatusForm.select(LaborStatusForm.department).where(LaborStatusForm.studentSupervisee == id).distinct()
        if supervisorID:
            authorizedUser = False
            status = Status.get(Status.statusName == "Approved")
            allUserDepartments = FormHistory.select(FormHistory.formID.department).join_from(FormHistory, LaborStatusForm).where((FormHistory.formID.supervisor == supervisorID) | (FormHistory.createdBy == UserID)).distinct()
            for userDepartment in allUserDepartments:
                for studentDepartment in allStudentDepartments:
                    if userDepartment.formID.department == studentDepartment.department:
                        authorizedUser = True
                        break

            for i in allUserDepartments:
                departmentsList.append(i.formID.department.departmentID)
            return(authorizedUser, departmentsList)
        else:
            for form in allStudentDepartments:
                departmentsList.append(form.department.departmentID)
            return departmentsList
    except Exception as e:
        print('Error authorizing user to access students labor history', type(e).__name__, e)
        raise type(e)
