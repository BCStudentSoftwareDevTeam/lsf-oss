#LSF file all caps fields are pulled from TRACY
#Modeled after Form.py in Advancement Office
from app.models import *
from app.models.term import Term
from app.models.student import Student
from app.models.user import User
from app.models.department import Department

#Any foreign keys^^^
#Any other imports

# NOTE: Always start classes with a capital letter
class LaborStatusForm (baseModel):
    laborStatusFormID           = IntegerField(primary_key = True)
    termCode                    = ForeignKeyField(Term)#FK to term
    studentSupervisee           = ForeignKeyField(Student)  #foreign key to student
    primarySupervisor           = ForeignKeyField(User) #foreign key to user
    department                  = ForeignKeyField(Department) #Foreign key to department
    secondarySupervisor         = ForeignKeyField(User, null=True)#student may not always have a secondary
    jobType                     = CharField() #Primary or secondary
    WLS                         = CharField() #pulled from tracy
    POSN_TITLE                  = CharField() #pulled from tracy eg. student programmer, customer engagement specialist, receptionist, teaching assistant
    POSN_CODE                   = CharField() #pulled from tracy
    contractHours               = IntegerField(null = True) #total hours for break terms
    weeklyHours                 = IntegerField(null = True) #weekly hours 10,12,15...
    startDate                   = CharField(null = True) #in case they start different than term start date
    endDate                     = CharField(null = True)
    supervisorNotes             = CharField(null=True) #null=True allows saving of null in db, and a supervisor may not always have notes
    laborDepartmentNotes        = CharField(null=True)


    def __str__(self):
        return str(self.__dict__)


# Scott: Skip queries for now.

#Queries as helper functions
####FIX ME: these are currently written as if they were in a class. Fix them to work with the laborStatusForm class
    # def select_all_laborStatusForms(self):
    #     try:
    #         laborStatusForms = self.laborStatusForm.select()
    #         return laborStatusForms
    #     except Exception as e:
    #       return False
    #
    # def select_single_laborStatusForm(self, laborStatusFormID):
    #     try:
    #       laborStatusForm = self.laborStatusForm.get(self.laborStatusForm.laborStatusFormID == laborStatusFormID)
    #       return laborStatusForm
    #     except Exception as e:
    #       print ("select_single_laborStatusForm",e)
    #       return False
    #
    # def insert_laborstatusForm(self, laborStatusFormID, primarySupervisor, createdDate, jobType, supervisee, supervisor,
    #                             creator, term, position, hours, startDate, endDate, supervisorNotes, laborDepartmentNotes):
    #     try:
    #         laborStatusForm = self.laborStatusForm(laborStatusFormID = laborStatusFormID, term = term, supervisee = supervisee, primarySupervisor = primarySupervisor,
    #                                         department = self.department, supervisor = supervisor, jobType = jobType, position = position,
    #                                         hours = hours, startDate = startDate, endDate = endDate, supervisorNotes = supervisorNotes,
    #                                         creator = creator,  createdDate = createdDate, laborDepartmentNotes = laborDepartmentNotes)
    #         laborStatusForm.save()
    #         return laborStatusForm
    #     except Exception as e:
    #          return e
