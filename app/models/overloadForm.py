#lsf File
from app.models import *
from app.models.user import User

class OverloadForm(baseModel):
    overloadReason          = CharField(primary_key=True)#Not sure if primary key
    financialAidApproved    = BooleanField()
    financialAidApprover    = ForeignKeyField(User)#Foreign key to USERS
    financialAidReviewDate  = DateField()
    SAASApproved            = BooleanField()
    SAASApprover            = ForeignKeyField(User)#Foreign key to USERS
    SAASReviewDate          = DateField()
    laborApproved           = BooleanField()
    laborApprover           = ForeignKeyField(User)#Foreign key to USERS
    laborReviewDate         = DateField()
