from app.models import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.laborReleaseForm import LaborReleaseForm
from app.models.modifiedForm import ModifiedForm
from app.models.overloadForm import OverloadForm
from app.models.status import Status
from app.models.user import User
from app.models.historyType import HistoryType

class FormHistory(baseModel):
    formHistoryID       = IntegerField(primary_key=True)
    formID              = ForeignKeyField(LaborStatusForm, on_delete="cascade")               # foreign key to lsf
    historyType         = ForeignKeyField(HistoryType)                                        # foreign key to historytype
    releaseForm         = ForeignKeyField(LaborReleaseForm, null=True, on_delete="SET NULL")  # if its a release form
    modifiedForm        = ForeignKeyField(ModifiedForm, null=True, on_delete="SET NULL")      # if its a form modification
    overloadForm        = ForeignKeyField(OverloadForm, null=True, on_delete="SET NULL")      # if its an overload application
    createdBy           = ForeignKeyField(User, related_name="creator",  on_delete="cascade") # Foreign key to USERS
    createdDate         = DateField()
    reviewedDate        = DateField(null=True)
    reviewedBy          = ForeignKeyField(User, null=True, related_name="reviewer",  on_delete="SET NULL") # Foreign key to USERS
    status              = ForeignKeyField(Status)                       # Foreign key to Status # Approved, rejected(or denied??), pending
    rejectReason        = CharField(null=True)                          # This should not be null IF that status is rejected
