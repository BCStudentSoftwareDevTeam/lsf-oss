from app.models import *
from peewee import CharField
# from app import login


class User(baseModel):
    username            = CharField(primary_key=True)
    firstname           = CharField(null=False)
    lastname            = CharField(null=False)
    # firstName           = CharField(null=False)
    # lastName            = CharField(null=False)
    # email               = CharField()
    # isLaborAdmin        = BooleanField()
    # isFinancialAidAdmin = BooleanField()
    # isSaasAdmin         = BooleanField()
# @login.user_loader
def load_user(username):
    return User.get(User.username == username)
