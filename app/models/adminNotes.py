from app.models import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.user import User

class AdminNotes(baseModel):
    noteHistoryID       = PrimaryKeyField()
    formID              = ForeignKeyField(LaborStatusForm, on_delete="cascade")               # foreign key to lsf
    createdBy           = ForeignKeyField(User, on_delete="cascade")
    notesContents       = CharField()
    date                = DateField()
