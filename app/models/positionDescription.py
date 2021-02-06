from app.models import *
from app.models.term import Term
from app.models.laborStatusForm import LaborStatusForm
from app.models.laborStatusForm import *


class PositionDescription (baseModel):
    positionDescriptionID         = PrimaryKeyField()
    termID                        = ForeignKeyField(Term, on_delete="cascade")
    POSN_CODE                     = CharField()
    positionDescription           = TextField(null=True)

    def __str__(self):
        return str(self.__dict__)
