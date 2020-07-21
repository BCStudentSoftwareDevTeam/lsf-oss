import pytest
from app.controllers.admin_routes.adminManagement import addAdmin, removeAdmin
from app.models.user import User
from peewee import DoesNotExist

@pytest.mark.integration
def test_addAdmin():
    isAdmin = 0

    newAdmin = "pearcej"
    user = User.get(User.username == newAdmin)

    # Test adding labor admin
    addAdmin(user, 'labor')
    assert user.isLaborAdmin != isAdmin

    # Test adding financial aid admin
    addAdmin(user, 'finAid')
    assert user.isFinancialAidAdmin != isAdmin

    # Test adding saas admin
    addAdmin(user, 'saas')
    assert user.isSaasAdmin != isAdmin

@pytest.mark.integration
def test_removeAdmin():
    isAdmin = 1

    oldAdmin = "pearcej"
    user = User.get(User.username == oldAdmin)

    # Test removing labor admin
    removeAdmin(user, 'labor')
    assert user.isLaborAdmin != isAdmin

    # Test removing financial aid admin
    removeAdmin(user, 'finAid')
    assert user.isFinancialAidAdmin != isAdmin

    # Test removing saas admin
    removeAdmin(user, 'saas')
    assert user.isSaasAdmin != isAdmin
