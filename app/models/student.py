from app.models.util import *
from app.models.user import *
#Any foreign keys or other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want
class student (baseModel):
    bNumber                         = CharField(primary_key=True)
    firstName                       = CharField()
    lastName                        = CharField()
    email                           = CharField()
    lastSupervisorUsername          = ForeignKeyField(user)

    def __str__(self):
        return str(self.bNumber)

#Queries as helper functions
####FIX ME: these are currently written as if they were in a class. Fix them to work with the laborStatusForm class
