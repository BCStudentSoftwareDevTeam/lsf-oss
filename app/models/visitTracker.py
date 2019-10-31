from app.models import *
from app.models.Tracy.studata import STUDATA
from app.models.student import Student


# All caps fields are pulled from TRACY
class VisitTracker (baseModel):
    officeVisitID       = PrimaryKeyField()
    ID                  = CharField(null=True)# B-number
    FIRST_NAME          = CharField(null=True)
    LAST_NAME           = CharField(null=True)
    reason              = CharField(null=True) #Paycheck, Direct deposit, etc, Other. If Other, store the "other" reason the user entered here
    isStudent           = BooleanFields(null=True) #If someone has a b#, this flag should be set to True.
    #There are cases in which staff comes in, though, and they DO have B#s. Ahad and Kat said they could indicate this rare case in the comments if its really necessary, but this flag is moreso for tracking non-BC affiliated visits
    comments            = Charfield(null=True)

    def __str__(self):
        return str(self.__dict__)
