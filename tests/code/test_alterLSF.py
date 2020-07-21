import pytest
from app.controllers.main_routes.alterLSF import modifyLSF, adjustLSF
from app.models.user import User
from app.models.laborStatusForm import LaborStatusForm
from app.models.adminNotes import AdminNotes
from app.models.adjustedForm import AdjustedForm
from app.models.formHistory import FormHistory

currentUser = User.get(User.userID == 1) # Scott Heggen's entry in User table
LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 2)
rsp = {'supervisor':{'oldValue':'B12361006', 'newValue':'B12365892','date':'07/21/2020'},
       'weeklyHours':{'oldValue': '20', 'newValue': '10', 'date': '07/21/2020'},
       'position':{'oldValue': 'S61419', 'newValue': 'S61407', 'date': '07/21/2020'},
       'supervisorNotes':{'oldValue':'old notes.', 'newValue':'new notes.'}
       }

@pytest.mark.integration
def test_modifyLSF():

    k = 'supervisorNotes'
    modifyLSF(rsp, k, LSF, currentUser)
    assert LSF.supervisorNotes == 'new notes.'

    k = 'supervisor'
    modifyLSF(rsp, k, LSF, currentUser)
    assert LSF.supervisor.ID == 'B12365892'

    k = 'position'
    modifyLSF(rsp, k, LSF, currentUser)
    assert LSF.POSN_CODE == 'S61407'

    k = 'weeklyHours'
    modifyLSF(rsp, k, LSF, currentUser)
    assert LSF.weeklyHours == 10

@pytest.mark.integration
def test_adjustLSF():

    k = 'supervisorNotes'
    adjustLSF(rsp, k, LSF, currentUser)
    assert AdminNotes.get(AdminNotes.notesContents == 'new notes.')

    k = 'supervisor'
    adjustLSF(rsp, k, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == k)
    assert adjustedForm.oldValue == 'B12361006'
    assert adjustedForm.newValue == 'B12365892'

@pytest.mark.integration
def createOverloadForm():
    # Honestly I am very lost here
    # I don't know why this test is not even called when I run monitor.sh
    k = 'weeklyHours'
    createOverloadForm(rsp, k ,LSF, currentUser, adjustedForm, formHistories)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == k)
    formHistories = FormHistory.get(FormHistory.historyType)
    assert adjustedForm.oldValue == 20
    assert adjustedForm.newValue == 10
    assert formHistories == 'Labor Adjustment Form'
