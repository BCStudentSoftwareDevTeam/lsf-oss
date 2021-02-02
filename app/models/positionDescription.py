from app.models import *
from app.models.laborStatusForm import LaborStatusForm


class PositionDescription (baseModel):
    positionDescriptionPrimaryKey = CompositeKey("LaborStatusForm.termCode", "LaborStatusForm.POSN_CODE")
    termID                        = PrimaryKeyField()
    POSN_CODE                     = PrimaryKeyField()
    positionDescription           = TextField(null=True)

    def __str__(self):
        return str(self.__dict__)
