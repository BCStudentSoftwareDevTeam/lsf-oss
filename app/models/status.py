from app.models import *


class Status(baseModel):
    statusName         = CharField(primary_key=True) # Approved, denied, pending, pre-student approval
