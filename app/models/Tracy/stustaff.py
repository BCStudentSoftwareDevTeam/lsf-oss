#THIS IS A TRACY FILE! NO TOUCHY!
from app.models.Tracy import *


class STUSTAFF(baseModel):
    PIDM        = PrimaryKeyField() 
    ID          = CharField(null=True) # B-number
    FIRST_NAME  = CharField(null=True)
    LAST_NAME   = CharField(null=True)
    EMAIL       = CharField(null=True)
    CPO         = CharField(null=True)
    ORG         = CharField(null=True)
    DEPT_NAME   = CharField(null=True)

    def __str__(self):
        return str(self.__dict__)
