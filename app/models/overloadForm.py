#lsf File
from app.models import *
from app.models.user import User

class OverloadForm(baseModel):
    overloadReason          = CharField(primary_key=True)#Not sure if primary key
    financialAidApproved    = BooleanField(null=True)
    financialAidApprover    = ForeignKeyField(User, null=True, on_delete="cascade")#Foreign key to USERS
    financialAidReviewDate  = DateField(null=True)
    SAASApproved            = BooleanField(null=True)
    SAASApprover            = ForeignKeyField(User, null=True, on_delete="cascade")#Foreign key to USERS
    SAASReviewDate          = DateField(null=True)
    laborApproved           = BooleanField(null=True)
    laborApprover           = ForeignKeyField(User, null=True, on_delete="cascade")#Foreign key to USERS
    laborReviewDate         = DateField(null=True)

