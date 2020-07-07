from app.models import *


#Capitalized fields are originally from Tracy
class Student(baseModel):
    ID              = CharField(primary_key=True)		        # B-number
    PIDM            = IntegerField(null=True)                  # from Tracy
    FIRST_NAME      = CharField(null=True)
    LAST_NAME       = CharField(null=True)
    CLASS_LEVEL     = CharField(null=True)
    ACADEMIC_FOCUS  = CharField(null=True)
    MAJOR           = CharField(null=True)
    PROBATION       = CharField(null=True)
    ADVISOR         = CharField(null=True)
    STU_EMAIL       = CharField(null=True)
    STU_CPO         = CharField(null=True)
    LAST_POSN     	= CharField(null=True)
    LAST_SUP_PIDM   = CharField(null=True)

    def __str__(self):
        return str(self.__dict__)
