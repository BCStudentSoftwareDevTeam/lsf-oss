# import the modules,
import pytest
from app import app
from app.models.user import User
from app.models.overloadForm import *
from app.models.term import *
from app.controllers.main_routes import studentOverloadApp
from app.logic.userInsertFunctions import *
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

print("LSF: ", lsf)
@pytest.mark.integration
def test_createOverloadFormAndFormHistory():
    """ The above function is from the UserInsert Funtions.py"""
    adjustLSF(fieldsChangedOverload, fieldName, lsf, currentUser)
    overload = createOverloadFormAndFormHistory(rspFunctional, lsf, currentUser, status)
    print("OverLoad form passed:", overload)

@pytest.mark.integration
def test_formCompletetion():
    """This function tests form completion"""
    pass

@pytest.mark.integration
def test_approval():
    """ This is for testing financial and approval"""
    pass

@pytest.mark.integration
def test_denied():
    """ This is for testing financial and disapproval"""
    pass
