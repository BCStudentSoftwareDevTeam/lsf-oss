from app.models import *
from app.models.laborStatusForm import LaborStatusForm

class EmailTracker(baseModel):
    formHistoryID       = PrimaryKeyField()
    formID              = ForeignKeyField(LaborStatusForm, on_delete="cascade")               # foreign key to lsf
    date                = DateField()
    recipient           = CharField()
