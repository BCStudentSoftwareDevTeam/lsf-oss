import pytest
from app.controllers.main_routes.alterLSF import modifyLSF, adjustLSF
from app.models.user import User
from app.models.laborStatusForm import LaborStatusForm
from app.models.adminNotes import AdminNotes
from app.models.adjustedForm import AdjustedForm
from app.models.formHistory import FormHistory

#  TODO : At the beginning of the file clean up the records we are creating.
@pytest.fixture
def setup():
    db_cleanup()
    yield

@pytest.fixture
def cleanup():
    yield
    db_cleanup()

def db_cleanup():
    AdminNotes.delete().where(AdminNotes.formID.cast('char').contains("9")).execute()
    FormHistory.delete().where((FormHistory.formID == 9) & (FormHistory.historyType != 'Labor Status Form')).execute()
    # AdjustedForm.delete().where(AdjustedForm.formID == 8).execute()



currentUser = User.get(User.userID == 1) # Scott Heggen's entry in User table
LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 9)
rsp = {'supervisor':{'oldValue':'B12361006', 'newValue':'B12365892','date':'07/21/2020'},
       'weeklyHours':{'oldValue': '10', 'newValue': '12', 'date': '07/21/2020'},
       'position':{'oldValue': 'S61419', 'newValue': 'S61407', 'date': '07/21/2020'},
       'supervisorNotes':{'oldValue':'old notes.', 'newValue':'new notes.'}
       }

rsp_overload = {'weeklyHours': {'oldValue':'10', 'newValue':'20'}}

@pytest.mark.integration
def test_modifyLSF(setup, cleanup):

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

    # # Overload hours created
    # k = 'weeklyHours'
    # modifyLSF(rsp_overload, k, LSF, currentUser)
    # assert LSF.weeklyHours == 20

@pytest.mark.integration
def test_adjustLSF(setup, cleanup):

    k = 'supervisorNotes'
    adjustLSF(rsp, k, LSF, currentUser)
    assert AdminNotes.get(AdminNotes.notesContents == 'new notes.')

    k = 'supervisor'
    adjustLSF(rsp, k, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == k)
    assert adjustedForm.oldValue == 'B12361006'
    assert adjustedForm.newValue == 'B12365892'

    k = 'position'
    adjustLSF(rsp, k, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == k)
    assert adjustedForm.oldValue == 'S61419'
    assert adjustedForm.newValue == 'S61407'

    k = 'weeklyHours'
    adjustLSF(rsp, k, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == k)
    assert adjustedForm.oldValue == '12'
    assert adjustedForm.newValue == '10'


# @pytest.mark.integration
# def createOverloadForm():
#     k = 'weeklyHours'
#     createOverloadForm(rsp, k ,LSF, currentUser, adjustedForm, formHistories)
#     adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == k)
#     formHistories = FormHistory.get(FormHistory.historyType)
#     assert adjustedForm.oldValue == 20
#     assert adjustedForm.newValue == 10
#     assert formHistories == 'Labor Adjustment Form'
