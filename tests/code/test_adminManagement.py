import pytest
from app.controllers.admin_routes.adminManagement import addAdmin, removeAdmin
from app.models.user import User
from peewee import DoesNotExist

@pytest.mark.integration
def test_addAdmin():
    newAdmin = "pearcej"
    user = User.get(User.username == newAdmin)

    # Test adding labor admin
    addAdmin(user, 'labor')
    assert user.isLaborAdmin

    # Test adding financial aid admin
    addAdmin(user, 'finAid')
    assert user.isFinancialAidAdmin

    # Test adding saas admin
    addAdmin(user, 'saas')
    assert user.isSaasAdmin

@pytest.mark.integration
def test_removeAdmin():
    oldAdmin = "pearcej"
    user = User.get(User.username == oldAdmin)

    # Test removing labor admin
    removeAdmin(user, 'labor')
    assert not user.isLaborAdmin

    # Test removing financial aid admin
    removeAdmin(user, 'finAid')
    assert not user.isFinancialAidAdmin

    # Test removing saas admin
    removeAdmin(user, 'saas')
    assert not user.isSaasAdmin
