from app.models import *

#############################
# USERS
#############################
from app.models.user import User

users = [
     {
         "username": "heggens",
         "firstname": "Scott",
         "lastname": "Heggen"
     },
     {
        "username": "pearcej",
        "firstname": "Jan",
        "lastname": "Pearce"
     }
    ]

for user in users:
    try:
        u = User.get_or_create(username = user["username"], firstname = user["firstname"], lastname = user["lastname"])
    except:
        pass

#############################
# Labor Status Forms
#############################
from app.models.laborStatusForm import LaborStatusForm

#TODO To be continued...
