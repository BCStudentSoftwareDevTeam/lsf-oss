from app.models import *
from app.models.term import Term
from app.models.position import Position

class TermPositionDescription (baseModel):
    termPositionDescriptionID     = PrimaryKeyField()
    termCode                      = ForeignKeyField(Term, on_delete="cascade")
    POSN_CODE                     = ForeignKeyField(Position, on_delete="cascade")
    positionDescription           = TextField(null=True)

    def __str__(self):
        return str(self.__dict__)
