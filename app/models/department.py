#lsf File
from app.models import *

class Department(baseModel):
    DEPT_NAME   = CharField(primary_key=True) #foreign key to lsf #Capital attributes are pulled from TRACY
    ACCOUNT     = CharField(null=True)
    ORG         = CharField(null=True)
    departmentCompliance    = BooleanField()#True if in compliance, false if out of it
