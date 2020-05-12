#lsf File
from app.models import *
from app.models.user import User
from app.models.status import Status

class OverloadForm(baseModel):
    overloadFormID          = PrimaryKeyField()
    studentOverloadReason          = CharField(null=True)
    financialAidApproved    = ForeignKeyField(Status, null=True, on_delete="cascade") #Foreign key to status
    financialAidApprover    = ForeignKeyField(User, null=True, on_delete="cascade")#Foreign key to USERS
    financialAidReviewDate  = DateField(null=True)
    SAASApproved            = ForeignKeyField(Status, null=True, on_delete="cascade") #Foreign key to status
    SAASApprover            = ForeignKeyField(User, null=True, on_delete="cascade")#Foreign key to USERS
    SAASReviewDate          = DateField(null=True)
    laborApproved           = ForeignKeyField(Status, null=True, on_delete="cascade") #Foreign key to status
    laborApprover           = ForeignKeyField(User, null=True, on_delete="cascade")#Foreign key to USERS
    laborReviewDate         = DateField(null=True)
