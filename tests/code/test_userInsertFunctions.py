import pytest
from app.logic.userInsertFunctions import *

@pytest.mark.integration
def test_createSupervisorFromTracy():
    # Test fail conditions
    with pytest.raises(ValueError):
        supervisor = createSupervisorFromTracy()

    with pytest.raises(InvalidUserException):
        supervisor = createSupervisorFromTracy("B12361006")

    with pytest.raises(InvalidUserException):
        supervisor = createSupervisorFromTracy(username="B12361006")

    with pytest.raises(InvalidUserException):
        supervisor = createSupervisorFromTracy(bnumber="heggens")

    # Test success conditions
    supervisor = createSupervisorFromTracy(username="heggens", bnumber="B12361006")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(username="", bnumber="B12361006")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(bnumber="B12361006")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(username="heggens")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(username="heggens", bnumber="")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy("heggens")
    assert supervisor.FIRST_NAME == "Scott"

    # Tests getting a supervisor from TRACY that does not exist in the supervisor table
    supervisor = createSupervisorFromTracy(username="hoffmanm", bnumber="B1236237")
    assert supervisor.FIRST_NAME == "Megan"
    supervisor.delete_instance()

    supervisor = createSupervisorFromTracy(username="", bnumber="B1236237")
    assert supervisor.FIRST_NAME == "Megan"
    supervisor.delete_instance()

    supervisor = createSupervisorFromTracy(username="hoffmanm")
    assert supervisor.FIRST_NAME == "Megan"
    supervisor.delete_instance()

@pytest.mark.integration
def test_createStudentFromTracy():
    # Test fail conditions
    with pytest.raises(ValueError):
        supervisor = createStudentFromTracy()

    with pytest.raises(InvalidUserException):
        supervisor = createStudentFromTracy("B00730361")

    with pytest.raises(InvalidUserException):
        supervisor = createStudentFromTracy(username="B00730361")

    with pytest.raises(InvalidUserException):
        supervisor = createStudentFromTracy(bnumber="jamalie")

    # Test success conditions
    supervisor = createStudentFromTracy(username="jamalie", bnumber="B00730361")
    assert supervisor.FIRST_NAME == "Elaheh"

    supervisor = createStudentFromTracy(username="", bnumber="B00730361")
    assert supervisor.FIRST_NAME == "Elaheh"

    supervisor = createStudentFromTracy(bnumber="B00730361")
    assert supervisor.FIRST_NAME == "Elaheh"

    supervisor = createStudentFromTracy(username="jamalie")
    assert supervisor.FIRST_NAME == "Elaheh"

    supervisor = createStudentFromTracy(username="jamalie", bnumber="")
    assert supervisor.FIRST_NAME == "Elaheh"

    supervisor = createStudentFromTracy("jamalie")
    assert supervisor.FIRST_NAME == "Elaheh"

    # Tests getting a supervisor from TRACY that does not exist in the supervisor table
    supervisor = createStudentFromTracy(username="adamskg", bnumber="B00785329")
    assert supervisor.FIRST_NAME == "Kat"
    supervisor.delete_instance()

    supervisor = createStudentFromTracy(username="", bnumber="B00785329")
    assert supervisor.FIRST_NAME == "Kat"
    supervisor.delete_instance()

    supervisor = createStudentFromTracy(username="adamskg")
    assert supervisor.FIRST_NAME == "Kat"
    supervisor.delete_instance()
