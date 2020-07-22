import pytest
from app.controllers.admin_routes.adminManagement import addAdmin, removeAdmin
from app.models.user import User
from peewee import DoesNotExist

@pytest.mark.integration
def test_addAdmin():
    newAdmin = "pearcej"
    user = User.get(User.username == newAdmin)

    # Before adding user as admin
    assert user.isLaborAdmin != True
    # Test adding labor admin
    addAdmin(user, 'labor')
    assert user.isLaborAdmin

    assert user.isFinancialAidAdmin != True
    # Test adding financial aid admin
    addAdmin(user, 'finAid')
    assert user.isFinancialAidAdmin

    assert user.isSaasAdmin != True
    # Test adding saas admin
    addAdmin(user, 'saas')
    assert user.isSaasAdmin

@pytest.mark.integration
def test_removeAdmin():
    oldAdmin = "pearcej"
    user = User.get(User.username == oldAdmin)

    # Before removing user as admin
    assert user.isLaborAdmin == True
    # Test removing labor admin
    removeAdmin(user, 'labor')
    assert not user.isLaborAdmin

    assert user.isFinancialAidAdmin == True
    # Test removing financial aid admin
    removeAdmin(user, 'finAid')
    assert not user.isFinancialAidAdmin

    assert user.isSaasAdmin == True
    # Test removing saas admin
    removeAdmin(user, 'saas')
    assert not user.isSaasAdmin
