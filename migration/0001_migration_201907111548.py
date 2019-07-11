# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class User(peewee.Model):
    username = CharField(max_length=255, primary_key=True)
    firstname = CharField(max_length=255)
    lastname = CharField(max_length=255)
    class Meta:
        table_name = "user"


@snapshot.append
class LaborReleaseForm(peewee.Model):
    laborReleaseFormID = IntegerField(primary_key=True)
    term = CharField(max_length=255)
    studentSupervisee = snapshot.ForeignKeyField(backref='supervisee', index=True, model='user', on_delete='RESTRICT')
    primarySupervisor = snapshot.ForeignKeyField(backref='supervisee', index=True, model='user', on_delete='RESTRICT')
    secondarySupervisor = snapshot.ForeignKeyField(backref='supervisee', index=True, model='user', null=True, on_delete='RESTRICT')
    departmentCode = IntegerField()
    department = CharField(max_length=255)
    jobType = CharField(max_length=255)
    position = CharField(max_length=255)
    releaseDate = CharField(max_length=255)
    conditionAtRelease = CharField(max_length=255)
    reasonForRelease = CharField(max_length=255)
    creator = CharField(max_length=255)
    createdDate = CharField(max_length=255)
    processed = BooleanField(default=False)
    processedBy = CharField(max_length=255)
    supervisorNotes = CharField(max_length=255)
    laborDepartmentNotes = CharField(max_length=255, null=True)
    class Meta:
        table_name = "laborreleaseform"


@snapshot.append
class LaborStatusForm(peewee.Model):
    laborStatusFormID = IntegerField(primary_key=True)
    term = CharField(max_length=255)
    studentSupervisee = CharField(max_length=255)
    primarySupervisor = CharField(max_length=255)
    department = CharField(max_length=255)
    departmentCode = IntegerField()
    secondarySupervisor = CharField(max_length=255, null=True)
    jobType = CharField(max_length=255)
    position = CharField(max_length=255)
    SummerBreakHours = IntegerField(null=True)
    RegularTermHours = IntegerField(null=True)
    startDate = CharField(max_length=255)
    endDate = CharField(max_length=255)
    supervisorNotes = CharField(max_length=255, null=True)
    creator = CharField(max_length=255)
    createdDate = CharField(max_length=255)
    laborDepartmentNotes = CharField(max_length=255, null=True)
    formStatus = CharField(max_length=255)
    class Meta:
        table_name = "laborstatusform"


@snapshot.append
class Term(peewee.Model):
    termID = IntegerField(primary_key=True)
    termName = CharField(max_length=255)
    termCode = IntegerField()
    active = BooleanField()
    class Meta:
        table_name = "term"


