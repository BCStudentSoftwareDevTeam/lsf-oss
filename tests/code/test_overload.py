import pytest
from app import app
from app.models.user import User
from app.models.overloadForm import *
from app.models.term import *
from app.controllers.main_routes import studentOverloadApp
from app.logic.userInsertFunctions import *
from app.controllers.admin_routes.financialAidOverload import formDenial
from app.controllers.admin_routes.allPendingForms import laborAdminOverloadApproval
from datetime import datetime,date




# get the user
currentUser = User.get(User.userID == 1)
term = Term.get(Term.termCode == '202000')
overLoadrspFunctional = {'stuName': 'Guillermo Adams', 'stuBNumber': 'B00734292', 'stuPosition': 'DUMMY POSITION', 'stuPositionCode': 'S12345', 'stuJobType': 'Primary', 'stuWeeklyHours': 20, 'stuContractHours': None, 'stuWLS': '3', 'stuStartDate': '08/01/2020', 'stuEndDate': '05/01/2021', 'stuTermCode': '202000', 'stuNotes': '', 'stuLaborNotes': None, 'stuSupervisor': 'Scott Heggen', 'stuDepartment': 'Computer Science', 'stuDepartmentORG': '2114', 'stuSupervisorID': 'B12361006', 'isItOverloadForm': 'True', 'isTermBreak': False, 'stuTotalHours': 20}
overLoadLSF = createLaborStatusForm("B00734292", "B12361006", "1", term, overLoadrspFunctional)
status = "Pending"
secondaryRSP = {'stuName': 'Alex Bryant', 'stuBNumber': 'B00841417', 'stuPosition': 'DUMMY POSITION', 'stuPositionCode': 'S12345', 'stuJobType': 'Seconday', 'stuWeeklyHours': 10, 'stuContractHours': None, 'stuWLS': '3', 'stuStartDate': '08/01/2020', 'stuEndDate': '05/01/2021', 'stuTermCode': '202000', 'stuNotes': '', 'stuLaborNotes': None, 'stuSupervisor': 'Scott Heggen', 'stuDepartment': 'Computer Science', 'stuDepartmentORG': '2114', 'stuSupervisorID': 'B12361006', 'isTermBreak': False, 'stuTotalHours': 20}

@pytest.fixture
def resetApprovalStatus():
    "Resetting the Approval status "
    formHistory = FormHistory.get(FormHistory.formID == overLoadLSF.laborStatusFormID)
    overloadForm = OverloadForm.get(OverloadForm.overloadFormID == formHistory.overloadForm.overloadFormID)
    overloadForm.financialAidApproved = None
    overloadForm.save()
    overloadForm.SAASApproved= None
    overloadForm.save()
    overloadForm.laborApproved = None
    overloadForm.save()

    yield

@pytest.mark.integration
def test_createOverload():
    """ The above function is from the UserInsert Funtions.py"""
    with app.test_request_context():
        overload = createOverloadFormAndFormHistory(overLoadrspFunctional, overLoadLSF, currentUser, status)
        assert FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))

        # secondary forms
        with app.test_client() as c:
             totalHours = c.post("/laborstatusform/checktotalhours/202000/B00841417/10/NaN", json={})
             print("after")



@pytest.mark.integration
def test_formCompletion():
    """This function tests form completion"""
    formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
    with app.test_client() as c:
        studentApproval = c.post('/studentOverloadApp/update', json={
            str(overLoadLSF.laborStatusFormID): {"Notes": "This is my reason", "formID": formHistory.formHistoryID
        }})
        overloadForm = OverloadForm.get(OverloadForm.overloadFormID == formHistory.overloadForm)
        assert overloadForm.studentOverloadReason == "This is my reason"

@pytest.mark.integration
def test_approval():
    """ This is for testing Financial Aid and approval.
    Files: FiniancialAidOverload and """

    formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
    with app.test_request_context():
        currentUser.isFinancialAidAdmin = 1
        currentUser.save()
        print("here")
        status = 'approved'
        with app.test_client() as c:
            print("before adminapp")
            FinancialAidApproval = c.post('/admin/financialAidOverloadApproval/'+status, json={
            'formHistoryID': formHistory.formHistoryID, 'denialNote': "I approve this form for Financial Aid"
            })
            formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
            assert formHistory.overloadForm.financialAidApproved.statusName == "Approved"
            # Testing SAAS Approval
            currentUser.isFinancialAidAdmin = 0
            currentUser.save()
            currentUser.isSaasAdmin = 1
            currentUser.save()

            SASSApproval = c.post('/admin/financialAidOverloadApproval/'+status, json={
            'formHistoryID': formHistory.formHistoryID, 'denialNote': "Saas approved this form"
            })
            formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
            assert formHistory.overloadForm.SAASApproved.statusName == "Approved"
            currentUser.isSaasAdmin = 0
            currentUser.save()

            adminApproval = c.post('/admin/modalFormUpdate', json={
            'formHistoryID': formHistory.formHistoryID, 'adminNotes': 'Approved by me', 'status': 'Approved', 'formType': 'Overload'
            })

            formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
            assert formHistory.overloadForm.laborApproved.statusName == "Approved"




@pytest.mark.integration
def test_denied(resetApprovalStatus):
    """ This is for testing financial and disapproval"""

    formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
    with app.test_request_context():
        currentUser.isFinancialAidAdmin = 1
        currentUser.save()
        status = 'denied'
        with app.test_client() as c:
            FinancialAidDenial = c.post('/admin/financialAidOverloadApproval/'+status, json={
            'formHistoryID': formHistory.formHistoryID, 'denialNote': "I denied this form for Financial Aid"
            })
            formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
            assert formHistory.overloadForm.financialAidApproved.statusName == "Denied"
            # Testing SAAS Approval
            currentUser.isFinancialAidAdmin = 0
            currentUser.save()
            currentUser.isSaasAdmin = 1
            currentUser.save()

            SaasDenial = c.post('/admin/financialAidOverloadApproval/'+status, json={
            'formHistoryID': formHistory.formHistoryID, 'denialNote': "Saas denied this form"
            })
            formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
            assert formHistory.overloadForm.SAASApproved.statusName == "Denied"

            #Testing for Labor Admin approval
            currentUser.isSaasAdmin = 0
            currentUser.save()

            adminDenial = c.post('/admin/modalFormUpdate', json={
            'formHistoryID': formHistory.formHistoryID, 'adminNotes': 'Denied by me', 'status': 'Denied', 'formType': 'Overload'
            })

            formHistory = FormHistory.get((FormHistory.formID == overLoadLSF.laborStatusFormID) & (FormHistory.historyType == "Labor Overload Form"))
            assert formHistory.overloadForm.laborApproved.statusName == "Denied"
