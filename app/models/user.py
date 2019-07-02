#Modeled after User.py in Advancement Office
from app.models.util import *
#Any foreign keys or other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want
class user (baseModel):
    username                    = CharField(primary_key=True)
    firstName                   = CharField(max_length=100)
    lastName                    = CharField(max_length=100)
    isAdmin                     = BooleanField(default=False)

    def __str__(self):
        return str(self.username)

#Queries as helper functions to user class
####FIX ME: these are currently written as if they were in a class. FIx them to work with the laborStatusForm class
def select_all_users(self):
    try:
        users = user.select().order_by(user.lastName)
        return users
    except Exception as e:
        raise False
def select_single_user(self):
    try:
        users = user.get(user.username == username)
        return users
    except Exception as e:
        print ("select_single_user",e)
        raise False
def insert_user(self):
     '''An insert query to add a new user.
     Args:  username  (str):  The user's username
            firstName (str):  The user's firstname
            lastName  (str):  The user's lastname
            isAdmin (bool):  Admin status true or false
    Return:
      status: True if successful, False if unsuccessful'''

    strings = [username,firstName,lastName]
    bools  = [isAdmin]
    if checkStrings(strings) and checkBooleans(bools):
      try:
        user = user(username=username,  firstname=firstName, lastname=lastName, isAdmin=isAdmin)
        user.save(force_insert=True)
        return True
      except Exception as e:
        print ("insert_user",e)
    return False
