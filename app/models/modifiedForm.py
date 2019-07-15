#lsf File
from app.models import *

class ModifiedForm(baseModel):
    fieldModified           = CharField(primary_key=True)#Not sure if primary key
    oldValue                = CharField()
    newValue                = CharField()
    effectiveDate           = DateField()
