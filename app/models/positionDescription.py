from app.models import *
from app.models.term import term

class PositionDescription:
    positionDescriptionID = PrimaryKeyField()
    termCode              = ForeignKeyField(null=False)
    positionDescription   = TextField(null=True)
