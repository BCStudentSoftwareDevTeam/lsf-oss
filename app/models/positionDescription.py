from app.models import *
from app.models.user import User
from app.models.status import Status
from app.models.position import Position

class PositionDescription (baseModel):
    positionDescriptionID         = PrimaryKeyField()
    createdBy                     = ForeignKeyField(User, on_delete="cascade")
    status                        = ForeignKeyField(Status)
    POSN_CODE                     = ForeignKeyField(Position)
    createdDate                   = DateField()
    endDate                       = DateField(null=True)

    def __str__(self):
        return str(self.__dict__)
