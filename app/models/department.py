from app.models import *

#Capital attributes are originally pulled from TRACY
class Department(baseModel):
    departmentID            = IntegerField(primary_key=True)
    DEPT_NAME               = CharField()
    ACCOUNT                 = CharField(null=True)
    ORG                     = CharField(null=True)
    departmentCompliance    = BooleanField()    # True if in compliance, false if out of it
