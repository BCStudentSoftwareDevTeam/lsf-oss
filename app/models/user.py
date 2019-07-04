from app.models import *
from peewee import CharField
# from app import login


class User(baseModel):
    username  = CharField(primary_key = True)
    firstname = CharField(null = False)

# @login.user_loader
def load_user(username):
    return User.get(User.username == username)
