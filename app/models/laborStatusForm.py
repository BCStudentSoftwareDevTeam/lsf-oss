#Modeled after Form.py in Advancement Office
from app.models import *

#Any foreign keys^^^
#Any other imports

# NOTE: Always start classes with a capital letter
class LaborStatusForm (baseModel):
    laborStatusFormID           = IntegerField(primary_key = True)
    term                        = CharField() #foreign key
    studentSupervisee           = CharField()  # foreign key to Student or user table (not sure which yet)
    primarySupervisor           = CharField() #foreign key to user???
    department                  = CharField()
    departmentCode              = IntegerField()
    secondarySupervisor         = CharField(null = True)
    jobType                     = CharField()
    position                    = CharField()
    SummerBreakHours            = IntegerField(null = True) # do we need a separate for per week for regular terms and total for summer??? Eg weeklyHours and totalHours?
    RegularTermHours            = IntegerField(null = True)
    startDate                   = CharField()
    endDate                     = CharField()
    supervisorNotes             = CharField(null=True) #null=True allows saving of null in db, and a supervisor may not always have notes
    creator                     = CharField()
    createdDate                 = CharField()
    laborDepartmentNotes        = CharField(null=True)
    formStatus                  = CharField(null=False)   # Store the state of the form, e.g., pending, approved, denied

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
