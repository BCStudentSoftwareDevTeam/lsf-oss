#Modeled after separate py file structure in Advancement Office
from app.models.util import *
from app.models.student import *
from app.models.user import *
#Any foreign keys or other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want

class laborReleaseForm (baseModel):
    laborReleaseFormID          = IntegerField(primary_key = True) #I THINK this is the primary key
    term                        = CharField() #foriegn key or banner??
    supervisee                  = CharField() #is this the student? can we change it to....student?Foreign key to students b#?
    primarySupervisor           = Charfield()#foreign key to user?
    department                  = Charfield()
    supervisor                  = CharField() #how is this different from primary supervisor?
                                            #is this strictly for secondary? this field should reflect that (secondarySupervisor)
                                            #if it is just for secodary supervisor, this should be null=True..
    ####I think this fom should just have 1 supervisor field. I dont think there's a spot to differentiate
    ###between primary and secondary supervisor, since that distinction is made in the position field
    jobType                     = CharField()#primary or secondary
    position                    = CharField()
    releaseDate                 = CharField()
    conditionAtRelease          = Charfield()#performance
    reasonForRelease            = CharField()
    creator                     = CharField()#i think this can be taken out
    createdDate                 = CharField()#I think this can be taken out too...??
    processedBy                 = Charfield()
    laborDepartmentNotes        = Charfield(null=True)#delete if redundant

    def __str__(self):
        return str(self.laborReleaseFormID)

#Queries as helper functions


def insert_laborReleaseForm(self, laborReleaseFormID, term, supervisee, primarySupervisor, department, supervisor, jobType, position,
                            releaseDate, reasonForRelease, creator, createdDate, processedBy, laborDepartmentNotes):
    try:
        laborReleaseForm = laborReleaseForm(laborReleaseFormID = laborReleaseFormID, term = term, supervisee = supervisee, primarySupervisor = primarySupervisor,
                                            department = department, supervisor = supervisor, jobType = jobType, position = position, releaseDate = releaseDate,
                                            reasonForRelease = reasonForRelease, creator = creator, createdDate = createdDate, processedBy = processedBy,
                                            laborDepartmentNotes = laborDepartmentNotes)
        laborReleaseForm.save()
        return laborReleaseForm
    except Exception as e:
         return e
