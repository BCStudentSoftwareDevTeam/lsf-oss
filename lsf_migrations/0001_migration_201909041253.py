# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Department(peewee.Model):
    departmentID = PrimaryKeyField(primary_key=True)
    DEPT_NAME = CharField(max_length=255)
    ACCOUNT = CharField(max_length=255, null=True)
    ORG = CharField(max_length=255, null=True)
    departmentCompliance = BooleanField(default=True)
    class Meta:
        table_name = "department"


@snapshot.append
class EmailTemplate(peewee.Model):
    emailTemplateID = PrimaryKeyField(primary_key=True)
    purpose = CharField(max_length=255)
    subject = CharField(max_length=255)
    body = CharField(max_length=255)
    audience = CharField(max_length=255)
    class Meta:
        table_name = "emailtemplate"


@snapshot.append
class Term(peewee.Model):
    termCode = IntegerField(primary_key=True)
    termName = CharField(max_length=255)
    termStart = DateField(null=True)
    termEnd = DateField(null=True)
    termState = BooleanField(default=False)
    class Meta:
        table_name = "term"


@snapshot.append
class Student(peewee.Model):
    ID = CharField(max_length=255, primary_key=True)
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
        table_name = "student"


@snapshot.append
class User(peewee.Model):
    username = CharField(max_length=255, primary_key=True)
    FIRST_NAME = CharField(max_length=255, null=True)
    LAST_NAME = CharField(max_length=255, null=True)
    EMAIL = CharField(max_length=255, null=True)
    CPO = CharField(max_length=255, null=True)
    ORG = CharField(max_length=255, null=True)
    DEPT_NAME = CharField(max_length=255, null=True)
    isLaborAdmin = BooleanField(null=True)
    isFinancialAidAdmin = BooleanField(null=True)
    isSaasAdmin = BooleanField(null=True)
    class Meta:
        table_name = "user"


@snapshot.append
class LaborStatusForm(peewee.Model):
    laborStatusFormID = PrimaryKeyField(primary_key=True)
    termCode = snapshot.ForeignKeyField(index=True, model='term', on_delete='cascade')
    studentSupervisee = snapshot.ForeignKeyField(index=True, model='student', on_delete='cascade')
    supervisor = snapshot.ForeignKeyField(index=True, model='user', on_delete='cascade')
    department = snapshot.ForeignKeyField(index=True, model='department', on_delete='cascade')
    jobType = CharField(max_length=255)
    WLS = CharField(max_length=255)
    POSN_TITLE = CharField(max_length=255)
    POSN_CODE = CharField(max_length=255)
    contractHours = IntegerField(null=True)
    weeklyHours = IntegerField(null=True)
    startDate = DateField(null=True)
    endDate = DateField(null=True)
    supervisorNotes = CharField(max_length=255, null=True)
    laborDepartmentNotes = CharField(max_length=255, null=True)
    class Meta:
        table_name = "laborstatusform"


@snapshot.append
class HistoryType(peewee.Model):
    historyTypeName = CharField(max_length=255, primary_key=True)
    class Meta:
        table_name = "historytype"


@snapshot.append
class LaborReleaseForm(peewee.Model):
    laborReleaseFormID = PrimaryKeyField(primary_key=True)
    conditionAtRelease = CharField(max_length=255)
    releaseDate = DateField()
    reasonForRelease = CharField(max_length=255)
    class Meta:
        table_name = "laborreleaseform"


@snapshot.append
class ModifiedForm(peewee.Model):
    modifiedFormID = PrimaryKeyField(primary_key=True)
    fieldModified = CharField(max_length=255)
    oldValue = CharField(max_length=255)
    newValue = CharField(max_length=255)
    effectiveDate = DateField()
    class Meta:
        table_name = "modifiedform"


@snapshot.append
class Status(peewee.Model):
    statusName = CharField(max_length=255, primary_key=True)
    class Meta:
        table_name = "status"


@snapshot.append
class OverloadForm(peewee.Model):
    overloadFormID = PrimaryKeyField(primary_key=True)
    overloadReason = CharField(max_length=255)
    financialAidApproved = snapshot.ForeignKeyField(index=True, model='status', null=True, on_delete='cascade')
    financialAidApprover = snapshot.ForeignKeyField(index=True, model='user', null=True, on_delete='cascade')
    financialAidReviewDate = DateField(null=True)
    SAASApproved = snapshot.ForeignKeyField(index=True, model='status', null=True, on_delete='cascade')
    SAASApprover = snapshot.ForeignKeyField(index=True, model='user', null=True, on_delete='cascade')
    SAASReviewDate = DateField(null=True)
    laborApproved = snapshot.ForeignKeyField(index=True, model='status', null=True, on_delete='cascade')
    laborApprover = snapshot.ForeignKeyField(index=True, model='user', null=True, on_delete='cascade')
    laborReviewDate = DateField(null=True)
    class Meta:
        table_name = "overloadform"


@snapshot.append
class FormHistory(peewee.Model):
    formHistoryID = PrimaryKeyField(primary_key=True)
    formID = snapshot.ForeignKeyField(index=True, model='laborstatusform', on_delete='cascade')
    historyType = snapshot.ForeignKeyField(index=True, model='historytype')
    releaseForm = snapshot.ForeignKeyField(index=True, model='laborreleaseform', null=True, on_delete='SET NULL')
    modifiedForm = snapshot.ForeignKeyField(index=True, model='modifiedform', null=True, on_delete='SET NULL')
    overloadForm = snapshot.ForeignKeyField(index=True, model='overloadform', null=True, on_delete='SET NULL')
    createdBy = snapshot.ForeignKeyField(backref='creator', index=True, model='user', on_delete='cascade')
    createdDate = DateField()
    reviewedDate = DateField(null=True)
    reviewedBy = snapshot.ForeignKeyField(backref='reviewer', index=True, model='user', null=True, on_delete='SET NULL')
    status = snapshot.ForeignKeyField(index=True, model='status')
    rejectReason = CharField(max_length=255, null=True)
    class Meta:
        table_name = "formhistory"


