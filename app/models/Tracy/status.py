#TRACY file
from app.models import *

class Status(baseModel):
  statusName         = CharField(primary_key=True) #Approved, rejected (or denied???), pending

