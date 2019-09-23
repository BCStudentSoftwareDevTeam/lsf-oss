# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class STUDATA(peewee.Model):
    PIDM = CharField(max_length=255, primary_key=True)
    ID = CharField(max_length=255, null=True)
    FIRST_NAME = CharField(max_length=255, null=True)
    LAST_NAME = CharField(max_length=255, null=True)
    CLASS_LEVEL = CharField(max_length=255, null=True)
    ACADEMIC_FOCUS = CharField(max_length=255, null=True)
    MAJOR = CharField(max_length=255, null=True)
    PROBATION = CharField(max_length=255, null=True)
    ADVISOR = CharField(max_length=255, null=True)
    STU_EMAIL = CharField(max_length=255, null=True)
    STU_CPO = CharField(max_length=255, null=True)
    LAST_POSN = CharField(max_length=255, null=True)
    LAST_SUP_PIDM = CharField(max_length=255, null=True)
    class Meta:
        table_name = "studata"


@snapshot.append
class STUPOSN(peewee.Model):
    POSN_CODE = CharField(max_length=255, primary_key=True)
    POSN_TITLE = CharField(max_length=255, null=True)
    WLS = CharField(max_length=255, null=True)
    ORG = CharField(max_length=255, null=True)
    ACCOUNT = CharField(max_length=255, null=True)
    DEPT_NAME = CharField(max_length=255, null=True)
    class Meta:
        table_name = "stuposn"


@snapshot.append
class STUSTAFF(peewee.Model):
    PIDM = CharField(max_length=255, primary_key=True)
    ID = CharField(max_length=255, null=True)
    FIRST_NAME = CharField(max_length=255, null=True)
    LAST_NAME = CharField(max_length=255, null=True)
    EMAIL = CharField(max_length=255, null=True)
    CPO = CharField(max_length=255, null=True)
    ORG = CharField(max_length=255, null=True)
    DEPT_NAME = CharField(max_length=255, null=True)
    class Meta:
        table_name = "stustaff"


