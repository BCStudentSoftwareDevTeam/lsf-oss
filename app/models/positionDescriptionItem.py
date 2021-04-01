from app.models import *
from app.models.position import Position

class PositionDescriptionItem (baseModel):
    positionDescriptionItemID     = PrimaryKeyField()
    positionDescription           = ForeignKeyField(Position, on_delete="cascade")
    itemDescription               = CharField()
    itemType                      = CharField()

    def __str__(self):
        return str(self.__dict__)
