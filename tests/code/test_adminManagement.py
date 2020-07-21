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
    assert user.isLaborAdmin != 0

    # Test adding financial aid admin
    addAdmin(user, 'finAid')
    assert user.isFinancialAidAdmin != 0

    # Test adding saas admin
    addAdmin(user, 'saas')
    assert user.isSaasAdmin != 0

@pytest.mark.integration
def test_removeAdmin():
    oldAdmin = "pearcej"
    user = User.get(User.username == oldAdmin)

    # Test removing labor admin
    removeAdmin(user, 'labor')
    assert user.isLaborAdmin != 1

    # Test removing financial aid admin
    removeAdmin(user, 'finAid')
    assert user.isFinancialAidAdmin != 1

    # Test removing saas admin
    removeAdmin(user, 'saas')
    assert user.isSaasAdmin != 1
