#Modeled after Form.py in Advancement Office
from app.models.util import *
#Any foreign keys
#Any other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want

class laborStatusForm (baseModel):
    formID                      = PrimaryKeyField() #I THINK this is the primary key
    term                        = CharField()
    supervisee                  = CharField() #is this the student? can we change it to....student?lmao
    primarySupervisor           = Charfield()
    department                  = Charfield()
    supervisor                  = CharField() #how is this different from primary supervisor? is this strictly for secondary? this field should reflect that (secondarySupervisor)
    jobType                     = CharField()
    position                    = CharField()
    hours                       = CharField() #do we need a separate for per week for regular terms and total for summer??? Eg weeklyHours and totalHours?
    startDate                   = CharField()
    endDate                     = CharField()
    supervisorNotes             = CharField()
    creator                     = CharField()
    createdDate                 = CharField()

    def __str__(self):
        return str(self.formID)
#Queries as helper functions
####FIX ME: these are currently written as if they were in a class. Fix them to work with the laborStatusForm class
def select_all_laborStatusForms(self):
    try:
        laborStatusForms = laborStatusForm.select()
        return laborStatusForms
    except Exception as e:
      return False

def select_single_laborStatusForm(self, formID):
    try:
      laborStatusForm = laborStatusForm.get(laborStatusForm.formID == formID)
      return laborStatusForm
    except Exception as e:
      print ("select_single_laborStatusForm",e)
      return False

def insert_laborstatusForm(self, formID, primarySupervisor, createdDate, jobType, supervisee, supervisor,
        creator, term, position, hours, startDate, endDate, supervisorNotes):
        try:
            laborStatusForm = laborStatusForm(formID = formID, term = term, supervisee = supervisee, primarySupervisor = primarySupervisor,
                                            department = department, supervisor = supervisor, jobType = jobType, position = position,
                                            hours = hours, startDate = startDate, endDate = endDate, supervisorNotes = supervisorNotes,
                                            creator = creator,  createdDate = createdDate)
            laborStatusForm.save()
            return laborStatusForm
        except Exception as e:
             return e
