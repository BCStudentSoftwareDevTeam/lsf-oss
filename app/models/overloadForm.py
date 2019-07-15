#lsf File
from app.models import *

class overloadForm(baseModel):
    overloadReason          = CharField(primary_key=True)#Not sure if primary key
    financialAidApproved    = BooleanField()
    financialAidApprover    = CharField()#foreign key to USERS
    financialAidReviewDate  = DateField()
    SAASApproved            = BooleanField()
    SAASApprover            = CharField()#foreign key to USERS
    SAASReviewDate          = DateField()
    laborApproved           = BooleanField()
    laborApprover           = CharField()#foreign key to USERS
    laborReviewDate         = DateField()
