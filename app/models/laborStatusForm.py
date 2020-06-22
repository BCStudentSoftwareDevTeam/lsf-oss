from app.models import *
from app.models.term import Term
from app.models.student import Student
from app.models.user import User
from app.models.department import Department


# All caps fields are pulled from TRACY
class LaborStatusForm (baseModel):
    studentName                 = CharField(null=True)
    laborStatusFormID           = PrimaryKeyField()
    termCode                    = ForeignKeyField(Term, on_delete="cascade")             # FK to term
    studentSupervisee           = ForeignKeyField(Student, on_delete="cascade")          # foreign key to student
    supervisor                  = ForeignKeyField(User, on_delete="cascade")             # foreign key to user
    department                  = ForeignKeyField(Department, on_delete="cascade")       # Foreign key to department
    #secondarySupervisor         = ForeignKeyField(User, null=True, on_delete="cascade")  # student may not always have a secondary #7/25/19: decided it was too                                                                                                 confusing language and we didnt even need to store this field..
    jobType                     = CharField()                       # Primary or secondary
    WLS                         = CharField()
    POSN_TITLE                  = CharField()                       # eg. student programmer, customer engagement specialist, receptionist, teaching assistant
    POSN_CODE                   = CharField()
    contractHours               = IntegerField(null=True)         # total hours for break terms
    weeklyHours                 = IntegerField(null=True)         # weekly hours 10,12,15...
    startDate                   = DateField(null=True)            # in case they start different than term start date
    endDate                     = DateField(null=True)
    supervisorNotes             = CharField(null=True)              # null=True allows saving of null in db, and a supervisor may not always have notes
    laborDepartmentNotes        = CharField(null=True)


    def __str__(self):
        return str(self.__dict__)
