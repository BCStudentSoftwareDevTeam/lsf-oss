import pytest
from app.logic.tracy import Tracy
from app.logic.tracy import InvalidQueryException

@pytest.fixture(scope='class')
def tracy(request):
    return Tracy()

@pytest.mark.usefixtures("tracy")
class Test_Tracy:

    @pytest.mark.unit
    def test_init(self, tracy):
        assert True

    @pytest.mark.integration
    def test_getStudents(self, tracy):
        students = tracy.getStudents()
        assert ['Alex','Elaheh','Guillermo','Kat'] == [s.FIRST_NAME for s in students]
        assert ['212','718','300','420'] == [s.STU_CPO for s in students]

    @pytest.mark.integration
    def test_getStudentFromBNumber(self, tracy):
        student = tracy.getStudentFromBNumber("B00734292")
        assert 'Guillermo' == student.FIRST_NAME

        with pytest.raises(InvalidQueryException):
            student = tracy.getStudentFromBNumber("B0000000")

        with pytest.raises(InvalidQueryException):
            student = tracy.getStudentFromBNumber(17)

    @pytest.mark.integration
    def test_getSupervisors(self, tracy):
        supervisors = tracy.getSupervisors()
        assert ['Brian','Jan','Jasmine','Mario','Megan','Scott'] == [s.FIRST_NAME for s in supervisors]
        assert ['6305','6301','6301','6302','6303','6300'] == [s.CPO for s in supervisors]

    @pytest.mark.integration
    def test_getSupervisorFromPIDM(self, tracy):
        supervisor = tracy.getSupervisorFromPIDM(4)
        assert 'Megan' == supervisor.FIRST_NAME

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromPIDM("eleven")

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromPIDM(17)

    @pytest.mark.integration
    def test_getSupervisorFromEmail(self, tracy):
        supervisor = tracy.getSupervisorFromEmail("nakazawam@berea.edu")
        assert 'Mario' == supervisor.FIRST_NAME

        supervisor = tracy.getSupervisorFromEmail("heggens@berea.edu")
        assert 'Scott' == supervisor.FIRST_NAME

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromEmail("nakazawamasdfd.com")

        with pytest.raises(InvalidQueryException):
            supervisor = tracy.getSupervisorFromEmail(17)

    @pytest.mark.integration
    def test_getPositionsFromDepartment(self, tracy):
        positions = tracy.getPositionsFromDepartment("Computer Science")

        assert ['S61408','S61407','S61421','S61419'] == [p.POSN_CODE for p in positions]

        positions = tracy.getPositionsFromDepartment("Underwater Basket-Weaving")
        assert [] == [p.POSN_CODE for p in positions]

    @pytest.mark.integration
    def test_getDepartments(self, tracy):
        departments = tracy.getDepartments()
        assert ['Biology','Computer Science','Mathematics','Technology and Applied Design'] == [d.DEPT_NAME for d in departments]
        assert '2107' == departments[0].ORG
        assert '6740' == departments[0].ACCOUNT

    @pytest.mark.integration
    def test_getPositionFromCode(self, tracy):
        position = tracy.getPositionFromCode("S61427")
        assert 'Teaching Associate' == position.POSN_TITLE
        assert '2' == position.WLS

        with pytest.raises(InvalidQueryException):
            position = tracy.getPositionFromCode("eleven")

        with pytest.raises(InvalidQueryException):
            position = tracy.getPositionFromCode(17)

