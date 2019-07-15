#lsf File
from app.models import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.laborReleaseForm import LaborReleaseForm
from app.models.modifiedForm import ModifiedForm
from app.models.overloadForm import OverloadForm
from app.models.status import Status
from app.models.user import User

class FormHistory(baseModel):
    formHistoryID       = IntegerField(primary_key=True)
    formID              = ForeignKeyField(column_name='laborStatusFormID', model=LaborStatusForm) #foreign key to lsf
    historyType         = CharField()#modified, released, overloaded
    releaseForm         = ForeignKeyField(LaborReleaseForm,null=True) #if its a release form
    modifiedForm        = ForeignKeyField(ModifiedForm,null=True) #if its a form modification
    overloadForm        = ForeignKeyField(OverloadForm,null=True) #if its an overload application
    createdBy           = ForeignKeyField(column_name='username', model=User)#Foreign key to USERS
    createdDate         = DateField()
    reviewedDate        = DateField()
    reviewedBy          = ForeignKeyField(column_name='username', model=User)#Foreign key to USERS
    status              = ForeignKeyField(column_name='statusName',model=Status)#Foreign key to Status #Approved, rejected(or denied??), pending
    rejectReason        = CharField() #This should not be null IF that status is rejected