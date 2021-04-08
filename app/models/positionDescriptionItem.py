from app.models import *
from app.models.positionDescription import PositionDescription

class PositionDescriptionItem (baseModel):
    positionDescriptionItemID     = PrimaryKeyField()
    positionDescription           = ForeignKeyField(PositionDescription, on_delete="cascade")
    itemDescription               = CharField()
    itemType                      = CharField()

    def __str__(self):
        return str(self.__dict__)
