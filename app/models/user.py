from app.models import *
from peewee import CharField
# from app import login


class User(baseModel):
    username  = CharField(primary_key=True)
    firstname = CharField(null=False)
    lastname  = CharField(null=False)
    #Was having trouble migrating so i just left this file alone. Below are new fields and theres a spot in add dummy to uncomment for new format
    # isLaborAdmin        = BooleanField(null=True)#Can be null, not every user will be an admin
    # isFinancialAid      = BooleanField(null=True)#Can be null, not every user (very few actually) will be Fin Aid
    # isSAAS              = BooleanField(null=True)#Can be null, not every user (very few actually) will be SAAS
# @login.user_loader
def load_user(username):
    return User.get(User.username == username)
