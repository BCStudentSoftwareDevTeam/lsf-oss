import pytest
from app.logic.userInsertFunctions import *

@pytest.mark.integration
def test_createSupervisorFromTracy():
    with pytest.raises(ValueError):
        supervisor = createSupervisorFromTracy()

    with pytest.raises(InvalidQueryException):
        supervisor = createSupervisorFromTracy("B12361006")

    with pytest.raises(InvalidQueryException):
        supervisor = createSupervisorFromTracy(username="B12361006")

    with pytest.raises(InvalidQueryException):
        supervisor = createSupervisorFromTracy(id="heggens")

    supervisor = createSupervisorFromTracy(username="heggens", id="B12361006")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(username="", id="B12361006")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(id="B12361006")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(username="heggens")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy(username="heggens", id="")
    assert supervisor.FIRST_NAME == "Scott"

    supervisor = createSupervisorFromTracy("heggens")
    assert supervisor.FIRST_NAME == "Scott"
