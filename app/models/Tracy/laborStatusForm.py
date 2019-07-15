#TRACY COPY FILE
from app.models import *

#Any foreign keys^^^
#Any other imports

# NOTE: Always start classes with a capital letter
class LaborStatusForm (baseModel):
    laborStatusFormID           = IntegerField(primary_key = True)
    term                        = CharField() #TODO: foreign key to term
    studentSupervisee           = CharField()  #foreign key to student
    primarySupervisor           = CharField() #foreign key to user
    department                  = CharField() #Foreign key to department
    secondarySupervisor         = CharField(null = True)
    jobType                     = CharField() #Primary or secondary
    positionWLS                 = CharField() #WLS level
    positionName                = CharField() #eg. student programmer, customer engagement specialist, receptionist, teaching assistant
    positionCode                = CharField()
    contractHours               = IntegerField(null = True) #total hours for break terms
    weeklyHours                 = IntegerField(null = True) #weekly hours 10,12,15...
    startDate                   = CharField(null = True) #in case they start different than term start date
    endDate                     = CharField(null = True)
    supervisorNotes             = CharField(null=True) #null=True allows saving of null in db, and a supervisor may not always have notes
    laborDepartmentNotes        = CharField(null=True)


    def __str__(self):
        return str(self.__dict__)
