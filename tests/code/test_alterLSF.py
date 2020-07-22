import pytest
from app.controllers.main_routes.alterLSF import modifyLSF, adjustLSF, createOverloadForm
from app.models.user import User
from app.models.laborStatusForm import LaborStatusForm
from app.models.adminNotes import AdminNotes
from app.models.adjustedForm import AdjustedForm
from app.models.formHistory import FormHistory

@pytest.fixture
def setup():
    delete_forms()
    yield

@pytest.fixture
def cleanup():
    yield
    delete_forms()


def delete_forms():
    formHistories = FormHistory.select().where((FormHistory.formID == 2) & (FormHistory.historyType == "Labor Adjustment Form"))
    for form in formHistories:
        AdjustedForm.delete().where(AdjustedForm.adjustedFormID == form.adjustedForm.adjustedFormID).execute()
        form.delete().execute()
    AdminNotes.delete().where(AdminNotes.formID.cast('char').contains("2")).execute()


currentUser = User.get(User.userID == 1) # Scott Heggen's entry in User table
LSF = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 2)
FieldsChanged = {'supervisor':{'oldValue':'B12361006', 'newValue':'B12365892','date':'07/21/2020'},
       'weeklyHours':{'oldValue': '10', 'newValue': '12', 'date': '07/21/2020'},
       'position':{'oldValue': 'S61419', 'newValue': 'S61407', 'date': '07/21/2020'},
       'supervisorNotes':{'oldValue':'old notes.', 'newValue':'new notes.'}
       }

FieldsChanged_overload = {'weeklyHours': {'oldValue':'10', 'newValue':'20', 'date': '07/21/2020'}}

FieldsChanged_contractHours = {'contractHours':{'oldValue': '40', 'newValue': '60', 'date': '07/21/2020'}}

@pytest.mark.integration
def test_modifyLSF(setup, cleanup):

    fieldName = 'supervisorNotes'
    modifyLSF(FieldsChanged, fieldName, LSF, currentUser)
    assert LSF.supervisorNotes == 'new notes.'

    fieldName = 'supervisor'
    modifyLSF(FieldsChanged, fieldName, LSF, currentUser)
    assert LSF.supervisor.ID == 'B12365892'

    fieldName = 'position'
    modifyLSF(FieldsChanged, fieldName, LSF, currentUser)
    assert LSF.POSN_CODE == 'S61407'

    fieldName = 'weeklyHours'
    modifyLSF(FieldsChanged, fieldName, LSF, currentUser)
    assert LSF.weeklyHours == 12

    fieldName = 'contractHours'
    modifyLSF(FieldsChanged_contractHours, fieldName, LSF, currentUser)
    assert LSF.contractHours == 60

@pytest.mark.integration
def test_adjustLSF(setup, cleanup):
    fieldName = 'supervisorNotes'
    adjustLSF(FieldsChanged, fieldName, LSF, currentUser)
    assert AdminNotes.get(AdminNotes.notesContents == 'new notes.')

    fieldName = 'supervisor'
    adjustLSF(FieldsChanged, fieldName, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
    assert adjustedForm.oldValue == 'B12361006'
    assert adjustedForm.newValue == 'B12365892'

    fieldName = 'position'
    adjustLSF(FieldsChanged, fieldName, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
    assert adjustedForm.oldValue == 'S61419'
    assert adjustedForm.newValue == 'S61407'

    fieldName = 'weeklyHours'
    adjustLSF(FieldsChanged, fieldName, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
    assert adjustedForm.oldValue == '10'
    assert adjustedForm.newValue == '12'

    fieldName = 'contractHours'
    adjustLSF(FieldsChanged_contractHours, fieldName, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
    assert adjustedForm.oldValue == '40'
    assert adjustedForm.newValue == '60'

@pytest.mark.integration
def test_overloadFormCreation(setup, cleanup):
    fieldName = 'weeklyHours'
    # Modified verload
    modifyLSF(FieldsChanged_overload, fieldName, LSF, currentUser)
    assert LSF.weeklyHours == 20
    formHistory = FormHistory.get((FormHistory.formID == LSF.laborStatusFormID) & (FormHistory.historyType == 'Labor Overload Form'))
    assert formHistory.historyType.historyTypeName == 'Labor Overload Form'

    # Adjusted Overload
    adjustLSF(FieldsChanged_overload, fieldName, LSF, currentUser)
    adjustedForm = AdjustedForm.get(AdjustedForm.fieldAdjusted == fieldName)
    assert adjustedForm.oldValue == '10'
    assert adjustedForm.newValue == '20'
    formHistory = FormHistory.get((FormHistory.formID == LSF.laborStatusFormID) & (FormHistory.historyType == 'Labor Overload Form'))
    assert formHistory.historyType.historyTypeName == 'Labor Overload Form'
