import pytest
from datetime import date, datetime
from app.logic.userInsertFunctions import *


@pytest.mark.integration
def testCreateLaborStatusForm():
    #lsf = createLaborStatusForm(studentID, primarySupervisor, department, term, rspFunctional)
    currentUser = User.get(User.userID == 1)
    lsf = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 2)
    assert lsf.termCode_id == 202000
    assert lsf.studentSupervisee_id == "B00841417"
    assert lsf.supervisor_id == "B12365892"
    assert lsf.department_id == 1
    assert lsf.jobType == "Primary"
    assert lsf.WLS == "1"
    assert lsf.POSN_TITLE == "Student Programmer"
    assert lsf.POSN_CODE == "S61407"
    assert lsf.contractHours == 60
    assert lsf.weeklyHours == 20
    assert lsf.startDate == datetime.strptime("04/01/2020", "%m/%d/%Y").strftime("%Y-%m-%d")
    assert lsf.endDate == datetime.strptime("09/01/2020", "%m/%d/%Y").strftime("%Y-%m-%d")
    assert lsf.supervisorNotes == "new notes."
    assert lsf.laborDepartmentNotes == None
    assert lsf.studentName == "Alex Bryant"
