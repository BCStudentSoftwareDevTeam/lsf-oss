#TRACY File
from app.models import *

class formHistory(baseModel):
    formID              = IntegerField(primary_key=True) #foreign key to lsf
    historyType         = CharField()#modified, released, overloaded
    releaseForm         = BooleanField(null=True) #if its a release form
    modifiedForm        = BooleanField(null=True) #if its a form modification
    overloadForm        = BooleanField(null=True) #if its an overload application
    createdBy           = CharField()#Foreign key to USERS
    createdDate         = DateField()
    reviewedDate        = DateField()
    reviewedBy          = CharField() #Foreign key to USERS
    status              = CharField() #Foreign key to Status #Approved, rejected(or denied??), pending
    rejectReason        = CharField() #This should not be null IF that status is rejected