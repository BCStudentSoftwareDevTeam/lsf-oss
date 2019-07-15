#lsf file
from app.models import *
#Any foreign keys or other imports

class Student(baseModel):#these things are from TRACY
    PIDM            = CharField(primary_key=True)		# Unique random ID
    ID              = CharField(null=True)		# B-number
    FIRST_NAME      = CharField(null=True)
    LAST_NAME       = CharField(null=True)
    CLASS_LEVEL     = CharField(null=True)
    ACADEMIC_FOCUS  = CharField(null=True)
    MAJOR           = CharField(null=True)
    PROBATION       = CharField(null=True)
    ADVISOR         = CharField(null=True)
    STU_EMAIL       = CharField(null=True)
    STU_CPO         = CharField(null=True)
    LAST_POSN   	= CharField(null=True)
    LAST_SUP_PIDM   = CharField(null=True)
    #any other TRACY info...
    def __str__(self):
        return str(self.__dict__)
