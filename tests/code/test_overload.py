# import the modules,
import pytest
from app import app
from app.models.user import User
from app.models.overloadForm import *
from app.models.term import *
from app.controllers.main_routes import studentOverloadApp
from app.logic.userInsertFunctions import *
from app.controllers.admin_routes.financialAidOverload import formDenial

@pytest.fixture
def setUp():
    delete_forms()
    yield


def delete_forms():
    """Find out forms which need to be deleted when we do the set up"""
    pass

# get the user
currentUser = User.get(User.userID == 1)
term = Term.get(Term.termCode == '202000')
rspFunctional = {'stuName': 'Guillermo Adams', 'stuBNumber': 'B00734292', 'stuPosition': 'DUMMY POSITION', 'stuPositionCode': 'S12345', 'stuJobType': 'Primary', 'stuWeeklyHours': 20, 'stuContractHours': None, 'stuWLS': '3', 'stuStartDate': '08/01/2020', 'stuEndDate': '05/01/2021', 'stuTermCode': '202000', 'stuNotes': '', 'stuLaborNotes': None, 'stuSupervisor': 'Scott Heggen', 'stuDepartment': 'Computer Science', 'stuDepartmentORG': '2114', 'stuSupervisorID': 'B12361006', 'isItOverloadForm': 'True', 'isTermBreak': False, 'stuTotalHours': 20}
lsf = createLaborStatusForm("B00734292", "B12361006", "1", term, rspFunctional)
status = "Pending"


@pytest.mark.integration
def test_createOverload():
    """ The above function is from the UserInsert Funtions.py"""
    with app.test_request_context():
        overload = createOverloadFormAndFormHistory(rspFunctional, lsf, currentUser, status)
        assert FormHistory.get((FormHistory.formID == lsf.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))

@pytest.mark.integration
def test_formCompletion():
    """This function tests form completion"""
    formHistory = FormHistory.get((FormHistory.formID == lsf.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
    with app.test_client() as c:
        rv = c.post('/studentOverloadApp/update', json={
            str(lsf.laborStatusFormID): {"Notes": "This is my reason", "formID": formHistory.formHistoryID
        }})
        overloadForm = OverloadForm.get(OverloadForm.overloadFormID == formHistory.overloadForm)
        assert overloadForm.studentOverloadReason == "This is my reason"

@pytest.mark.integration
def test_approval():
    """ This is for testing Financial Aid and approval"""
    with app.test_request_context():
        status = 'approved'
        currentUser.isFinancialAidAdmin = 1
        currentUser.save()
        formDenial(status)



@pytest.mark.integration
def test_denied():
    """ This is for testing financial and disapproval"""
    pass
