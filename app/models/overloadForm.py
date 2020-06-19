#lsf File
from app.models import *
from app.models.user import User
from app.models.status import Status
from app.models.supervisor import Supervisor

class OverloadForm(baseModel):
    overloadFormID          = PrimaryKeyField()
    studentOverloadReason   = CharField(null=True)
    financialAidApproved    = ForeignKeyField(Status, null=True, on_delete="cascade") #Foreign key to status
    financialAidApprover    = ForeignKeyField(Supervisor, null=True, on_delete="cascade")#Foreign key to Supervisor
    financialAidReviewDate  = DateField(null=True)
    SAASApproved            = ForeignKeyField(Status, null=True, on_delete="cascade") #Foreign key to status
    SAASApprover            = ForeignKeyField(Supervisor, null=True, on_delete="cascade")#Foreign key to Supervisor
    SAASReviewDate          = DateField(null=True)
    laborApproved           = ForeignKeyField(Status, null=True, on_delete="cascade") #Foreign key to status
    laborApprover           = ForeignKeyField(Supervisor, null=True, on_delete="cascade")#Foreign key to Supervisor
    laborReviewDate         = DateField(null=True)
