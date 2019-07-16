from app.models import *

#Capital attributes are originally pulled from TRACY
class Department(baseModel):
    DEPT_NAME               = CharField(primary_key=True)
    ACCOUNT                 = CharField(null=True)
    ORG                     = CharField(null=True)
    departmentCompliance    = BooleanField()    # True if in compliance, false if out of it
