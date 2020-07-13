import pytest
from app.logic.userInsertFunctions import *

@pytest.mark.integration
def test_createSupervisorFromTracy():
    supervisor = createSupervisorFromTracy(username="", id="B12361006")
    # assert type(supervisor) is <Model: Supervisor>
    assert type(supervisor) is Model
