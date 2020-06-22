from app.config.loadConfig import get_secret_cfg 
from peewee import DoesNotExist
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

    #######################################

    def __init__(self):
        secret_conf = get_secret_cfg()

    def getStudents(self):
        """
        Return a list of student objects sorted alphabetically by first name
        """
        return STUDATA.select().order_by(STUDATA.FIRST_NAME.asc())

    def getStudentFromBNumber(self, bnumber: str):
        """
        Return the student with the given B Number.

        Throws an InvalidQueryException if the B Number does not exist.
        """
        try:
            return STUDATA.get(STUDATA.ID == bnumber)
        except DoesNotExist:
            raise InvalidQueryException("B# {} not found in STUDATA".format(bnumber))

    #######################################

    def getSupervisors(self):
        """
        Return a list of supervisor objects sorted alphabetically by first name
        """
        return STUSTAFF.select().order_by(STUSTAFF.FIRST_NAME.asc())

    def getSupervisorFromPIDM(self, pidm: int):
        """
        Return the supervisor with the given PIDM.

        Throws an InvalidQueryException if the PIDM does not exist or an invalid value was given.
        """
        try:
            return STUSTAFF.get(STUSTAFF.PIDM == pidm)
        except DoesNotExist:
            raise InvalidQueryException("PIDM {} not found in STUSTAFF".format(pidm))
        except ValueError:
            raise InvalidQueryException("PIDM must be an integer".format(pidm))

    #######################################

    def getDepartments(self):
        """
        Return a list of departments, ordered by department name.
        """
        return STUPOSN.select(STUPOSN.ORG, STUPOSN.DEPT_NAME, STUPOSN.ACCOUNT).distinct().order_by(STUPOSN.DEPT_NAME.asc())

    def getPositionsFromDepartment(self, department: str):
        """
        Return a list of position objects for the given department name, sorted by position title
        """
        return STUPOSN.select().where(STUPOSN.DEPT_NAME == department).order_by(STUPOSN.POSN_TITLE.asc())

    def getPositionFromCode(self, positionCode: str):
        """
        Return the position for a given position code.
        """
        try:
            return STUPOSN.get(STUPOSN.POSN_CODE == positionCode)
        except DoesNotExist:
            raise InvalidQueryException("Position Code {} not found in STUPOSN".format(positionCode))
            
