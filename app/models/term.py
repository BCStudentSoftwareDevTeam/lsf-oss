######LSF Term File#####
#Modeled after User.py in Advancement Office with inspo from CAS models
from app.models import *
#Any foreign keys or other imports

class Term(baseModel):
    termCode            = IntegerField(primary_key=True) ## Term codes, like 201612 for Spring 2017. Matches Banner nomenclature Need to make new for AY.
    termName            = CharField(null=False) #Spring 2020 only, Summer, Chsirtmas Break, AY 2020-2021
    termStart           = DateField(null=False) #strtdate
    termEnd             = DateField(null=False) #enddate
    termState           = CharField(null=False)#open, closed, inactive
