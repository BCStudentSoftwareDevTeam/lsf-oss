from app.config.loadConfig import get_secret_cfg 
from peewee import DoesNotExist
from app.models.Tracy import db
from app.models.Tracy.stuposn import STUPOSN
from app.models.Tracy.studata import STUDATA
from app.models.Tracy.stustaff import STUSTAFF
from app import app

class InvalidQueryException(BaseException):
    pass

class Tracy():
    """
    A data access object for our Tracy queries.
    """

    def __init__(self):
        secret_conf = get_secret_cfg()

    #######################################

    def getStudents(self):
        """
        Return a list of student objects sorted alphabetically by first name
        """
        return STUDATA.query.order_by(STUDATA.FIRST_NAME).all()

    def getStudentFromBNumber(self, bnumber: str):
        """
        Return the student with the given B Number.

        Throws an InvalidQueryException if the B Number does not exist.
        """
        student = STUDATA.query.filter(STUDATA.ID == bnumber).first()
        if student is None:
            raise InvalidQueryException("B# {} not found in STUDATA".format(bnumber))

        return student

    #######################################

    def getSupervisors(self):
        """
        Return a list of supervisor objects sorted alphabetically by first name
        """
        return STUSTAFF.query.order_by(STUSTAFF.FIRST_NAME).all()

    def getSupervisorFromPIDM(self, pidm):
        """
        Return the supervisor with the given PIDM.

        Throws an InvalidQueryException if the given PIDM does not exist.
        """
        supervisor = STUSTAFF.query.get(pidm)
        if supervisor is None:
            raise InvalidQueryException("PIDM {} not found in STUSTAFF".format(pidm))

        return supervisor

    def getSupervisorFromEmail(self, email: str):
        """
        Return the supervisor with the given email.

        Throws an InvalidQueryException if the given email address does not exist.
        """
        supervisor = STUSTAFF.query.filter(STUSTAFF.EMAIL == email).first()
        if supervisor is None:
            raise InvalidQueryException("Email {} not found in STUSTAFF".format(email))

        return supervisor

    #######################################

    def getDepartments(self):
        """
        Return a list of departments, ordered by department name.
        """
        return STUPOSN.query.with_entities(STUPOSN.ORG, STUPOSN.DEPT_NAME, STUPOSN.ACCOUNT) \
                            .distinct().order_by(STUPOSN.DEPT_NAME).all()

    def getPositionsFromDepartment(self, department: str):
        """
        Return a list of position objects for the given department name, sorted by position title
        """
        return STUPOSN.query.filter(STUPOSN.DEPT_NAME == department).order_by(STUPOSN.POSN_TITLE).all()

    def getPositionFromCode(self, positionCode: str):
        """
        Return the position for a given position code.
        """
        position = STUPOSN.query.get(positionCode)
        if position is None:
            raise InvalidQueryException("Position Code {} not found in STUPOSN".format(positionCode))

        return position
            
