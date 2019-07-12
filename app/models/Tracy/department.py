#TRACY File
from app.models import *

class Department(baseModel):
    departmentName          = CharField(primary_key=True) #foreign key to lsf
    departmentAccount       = IntegerField()#I think these are numbers
    departmentOrg           = IntegerField()#I think these are numbers
    departmentCompliance    = BooleanField()#True if in compliance, false if out of it