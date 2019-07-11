#####TRACY USER FILE#######
from app.models import *
from peewee import CharField
# from app import login


class User(baseModel):
    supervisorUsername  = CharField(primary_key=True)
    firstName           = CharField(null=False)
    lastName            = CharField(null=False)
    email               = Charfield()
    isLaborAdmin        = Booleanfield()
    isFinancialAidAdmin = Booleanfield()
    isSaasAdmin         = Booleanfield()


# @login.user_loader
def load_user(username):
    return User.get(User.username == username)
