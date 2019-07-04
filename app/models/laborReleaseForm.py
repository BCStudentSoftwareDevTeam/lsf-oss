#Modeled after separate py file structure in Advancement Office
from app.models import *
from app.models.user import User

#Any foreign keys or other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want



class LaborReleaseForm (baseModel):
    laborReleaseFormID          = IntegerField(primary_key = True) #I THINK this is the primary key
    term                        = CharField() #foriegn key or banner??
    studentSupervisee           = ForeignKeyField(User, null = False, related_name='supervisee', on_delete= 'RESTRICT') #is this the student? can we change it to....student?Foreign key to students b#?
    primarySupervisor           = ForeignKeyField(User, null = False, related_name='supervisee', on_delete= 'RESTRICT')   # Primary supervisor
    secondarySupervisor         = ForeignKeyField(User, null = True, related_name='supervisee', on_delete= 'RESTRICT')
    departmentCode              = IntegerField()   # Org code
    department                  = CharField()   # Org name
    jobType                     = CharField()   # primary or secondary
    position                    = CharField()
    releaseDate                 = CharField()
    conditionAtRelease          = CharField()   # Performance (satisfactory or unsatisfactory
    reasonForRelease            = CharField()
    creator                     = CharField()   # Need for records tracking
    createdDate                 = CharField()   # Need for records tracking
    processed                 = BooleanField(null = False, default=False)  # Track if form has been processed by labor office
    processedBy                 = CharField()   # Need for records tracking
    supervisorNotes             = CharField()   # Allow supervisor to add additional notes in form
    laborDepartmentNotes        = CharField(null=True)  # Allow labor office to make notes about the form

    def __str__(self):
        return str(self.laborReleaseFormID)


    # I don't think simple functions like this are necessary.
    # Ones that are necessary involve modifying data before inserting/selecting
    # We'll see when we start actually using the models. Skip for now.
    def insert_laborReleaseForm(self, releaseFormObject):
        try:
            releaseFormObject.save()
            return True
        except Exception as e:
             print("Labor release Model error: ", e)
             return False
