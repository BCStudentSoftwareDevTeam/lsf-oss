#Modeled after Form.py in Advancement Office
from app.models.util import *
from app.models.student import *
from app.models.user import *
#Any foreign keys^^^
#Any other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want

class laborStatusForm (baseModel):
    laborStatusFormID           = IntegerField(primary_key = True)
    term                        = CharField() #foriegn key or banner??
    supervisee                  = CharField() #is this the student? can we change it to....student?Foreign key to students b#?
    primarySupervisor           = Charfield() #foreign key to user???
    department                  = Charfield()
    supervisor                  = CharField() #how is this different from primary supervisor?
                                            #is this strictly for secondary? this field should reflect that (secondarySupervisor)
                                            #if it is just for secodary supervisor, this should be null=True
    jobType                     = CharField()
    position                    = CharField()
    hours                       = CharField() #do we need a separate for per week for regular terms and total for summer??? Eg weeklyHours and totalHours?
    startDate                   = CharField()
    endDate                     = CharField()
    supervisorNotes             = CharField(null=True) #null=True allows saving of null in db, and a supervisor may not always have notes
    creator                     = CharField()
    createdDate                 = CharField()
    laborDepartmentNotes        = Charfield(null=True)#delete if redundant, but i think we need two spots for notes now

    def __str__(self):
        return str(self.laborStatusFormID)
#Queries as helper functions
####FIX ME: these are currently written as if they were in a class. Fix them to work with the laborStatusForm class
def select_all_laborStatusForms(self):
    try:
        laborStatusForms = laborStatusForm.select()
        return laborStatusForms
    except Exception as e:
      return False

def select_single_laborStatusForm(self, laborStatusFormID):
    try:
      laborStatusForm = laborStatusForm.get(laborStatusForm.laborStatusFormID == laborStatusFormID)
      return laborStatusForm
    except Exception as e:
      print ("select_single_laborStatusForm",e)
      return False

def insert_laborstatusForm(self, laborStatusFormID, primarySupervisor, createdDate, jobType, supervisee, supervisor,
                            creator, term, position, hours, startDate, endDate, supervisorNotes, laborDepartmentNotes):
    try:
        laborStatusForm = laborStatusForm(laborStatusFormID = laborStatusFormID, term = term, supervisee = supervisee, primarySupervisor = primarySupervisor,
                                        department = department, supervisor = supervisor, jobType = jobType, position = position,
                                        hours = hours, startDate = startDate, endDate = endDate, supervisorNotes = supervisorNotes,
                                        creator = creator,  createdDate = createdDate, laborDepartmentNotes = laborDepartmentNotes)
        laborStatusForm.save()
        return laborStatusForm
    except Exception as e:
         return e
