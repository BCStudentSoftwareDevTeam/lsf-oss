#Modeled after User.py in Advancement Office with inspo from CAS models
from app.models import *
#Any foreign keys or other imports

class Term(baseModel):
    termID  = IntegerField(primary_key=True)
    termName = CharField(null=False)
    termCode = IntegerField()       # Term codes, like 201612 for Spring 2017. Matches Banner nomenclature
    active = BooleanField()


