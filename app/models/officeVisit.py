from app.models import *
from app.models.Tracy.studata import STUDATA
from app.models.student import Student


# All caps fields are pulled from TRACY
class officeVisit (baseModel):
    officeVisitID       = PrimaryKeyField()
    ID   				= CharField(null=True)# B-number
	FIRST_NAME  		= CharField(null=True)
	LAST_NAME  			= CharField(null=True)
    reason              = CharField(null=True) #Paycheck, Direct deposit, etc, Other. If Other, "other" field will no longer be null and the reason eneterd by the user will be stored here.
    other               = CharField(null=True) #If the reason is other, this field will hold the reason
    comments            = CharField(null=True) #additional comment box below reason



    def __str__(self):
        return str(self.__dict__)
