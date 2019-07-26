from app.models import *


class LaborReleaseForm (baseModel):
    laborReleaseFormID          = PrimaryKeyField()
    conditionAtRelease          = CharField(null=False)          # Performance (satisfactory or unsatisfactory)
    releaseDate                 = DateField(null=False)          # Can be tomorrow's date or future date, never past date
    reasonForRelease            = CharField(null=False)

    def __str__(self):
        return str(self.laborReleaseFormID)
