from app.models import *

class HistoryType(baseModel):
    historyTypeName    = CharField(primary_key=True) # Labor Status Form, Labor Adustment Form, Labor Release Form, Labor Modified Form, Labor Overload Form
