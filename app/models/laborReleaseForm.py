#lsf file, not tracy
#Modeled after separate py file structure in Advancement Office
from app.models import *
#Any foreign keys or other imports

#Now relates to formHistory table
class LaborReleaseForm (baseModel):
    laborReleaseFormID          = IntegerField(primary_key = True) #I THINK this is the primary key
    conditionAtRelease          = CharField(null = False,)   # Performance (satisfactory or unsatisfactory)
    releaseDate                 = DateField(null = False,) #can be tomorrow's date of or futre date, never past date
    reasonForRelease            = CharField(null = False,)

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
