# import the modules,
import pytest
from app import app
from app.models.user import User
from app.models.overloadForm import *
from app.controllers.main_routes import studentOverload.py


@pytest.fixture
def setUp():
    delete_forms()
    yield


def delete_forms():
    """Find out forms which need to be deleted when we do the set up"""
    pass

# get the user


@pytest.mark.integration
def test_createOverloadFormAndFormHistory(rspFunctional[i], lsf, currentUser, status):
    """ The above function is from the UserInsert Funtions.py"""
    pass

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
