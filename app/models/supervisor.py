from app.models import *
from peewee import CharField
# from app import login


# Capitalized fields are originally pulled from tracy
class Supervisor(baseModel):
    UserID              = PrimaryKeyField()
    PIDM                = IntegerField(null=False)
    FIRST_NAME          = CharField(null=True)
    LAST_NAME           = CharField(null=True)
    ID                  = CharField(null=True)  #B-number
    EMAIL               = CharField(null=True)
    CPO                 = CharField(null=True)
    ORG                 = CharField(null=True)
    DEPT_NAME           = CharField(null=True)
