from app.models import *
from peewee import CharField
# from app import login


# Capitalized fields are originally pulled from tracy
class User(baseModel):
    username            = CharField(primary_key=True)
    FIRST_NAME          = CharField(null=True)
    LAST_NAME           = CharField(null=True)
    EMAIL               = CharField(null=True)
    CPO                 = CharField(null=True)
    ORG                 = CharField(null=True)
    DEPT_NAME           = CharField(null=True)
    isLaborAdmin        = BooleanField(null=True)
    isFinancialAidAdmin = BooleanField(null=True)
    isSaasAdmin         = BooleanField(null=True)

    def __str__(self):
        return str(self.__dict__)

# @login.user_loader
def load_user(username):
    return User.get(User.username == username)
