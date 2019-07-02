#Modeled after Form.py in Advancement Office
from app.models.util import *
#Any foreign keys
#Any other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want

class pastLaborStatusForm (baseModel):
    formID                      = PrimaryKeyField() #I THINK this is the primary key
    term                        = CharField()
    supervisee                  = CharField() #is this the student? can we change it to....student?lmao
    primarySupervisor           = CharField()
    department                  = CharField()
    supervisor                  = CharField() #how is this different from primary supervisor?
                                            #is this strictly for secondary? this field should reflect that (secondarySupervisor)
                                            #if it is just for secodary supervisor, this should be null=True
    jobType                     = CharField()
    position                    = CharField()
    hours                       = CharField() #do we need a separate for per week for regular terms and total for summer??? Eg weeklyHours and totalHours? PastLaborStatusForm.cs has WLS...
    startDate                   = CharField()
    endDate                     = CharField()
    supervisorNotes             = CharField(null=True) #null=True allows saving of null in db, and a supervisor may not always have notes
    creator                     = CharField()
    createdDate                 = CharField()
    laborDepartmentNotes        = CharField(null=True)#delete if redundant, but i think we need two spots for notes now
    processedBy                 = CharField()
    processedDate               = CharField()
    rejectReason                = CharField()
    #UNSURE ABOUT THESE BUT THEY WERE IN PASTLABORFORMS.cs
    #Department code
    #Department account
    #WLS
    #Positionc (i think this is a typo? it was in LSF.cs and PLSF.cs)
    def __str__(self):
        return str(self.formID)

#Queries as helper functions
####FIX ME: these are currently written as if they were in a class. FIx them to work with the laborStatusForm class

def select_all_pastLaborStatusForms(self):
    try:
        pastLaborStatusForms = pastLaborStatusForm.select()
        return pastLaborStatusForms
    except Exception as e:
      return False

def select_single_pastLaborStatusForm(self, formID):
    try:
      pastLaborStatusForm = pastLaborStatusForm.get(pastlaborStatusForm.formID == formID)
      return pastlaborStatusForm
    except Exception as e:
      print ("select_single_pastLaborStatusForm",e)
      return False
