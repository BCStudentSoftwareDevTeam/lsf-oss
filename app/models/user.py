#LSF file
from app.models import *
from peewee import CharField
# from app import login


class User(baseModel):
    username            = CharField(primary_key=True)
    # firstname           = CharField(null=False)
    # lastname            = CharField(null=False)#Still having trouble migrating so the updates are commented below.
    firstName           = CharField(null=False)
    lastName            = CharField(null=False)
    email               = CharField(null=True)
    isLaborAdmin        = BooleanField(null=True)
    isFinancialAidAdmin = BooleanField(null=True)
    isSaasAdmin         = BooleanField(null=True)
# @login.user_loader
def load_user(username):
    return User.get(User.username == username)
