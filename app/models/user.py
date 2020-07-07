from app.models import *
from app.models.student import Student
from app.models.supervisor import Supervisor
from peewee import CharField
# from app import login


# Capitalized fields are originally pulled from tracy
class User(baseModel):
    userID              = PrimaryKeyField()
    Student             = ForeignKeyField(Student, null=True)
    Supervisor          = ForeignKeyField(Supervisor, null=True)
    username            = CharField(null=False)
    isLaborAdmin        = BooleanField(null=True)
    isFinancialAidAdmin = BooleanField(null=True)
    isSaasAdmin         = BooleanField(null=True)

    def __str__(self):
        return str(self.__dict__)
