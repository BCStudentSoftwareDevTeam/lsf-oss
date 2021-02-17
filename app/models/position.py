from app.models import *

class Position (baseModel):

    POSN_CODE   = CharField(primary_key=True)
    POSN_TITLE  = CharField()
    WLS         = CharField()
    ORG         = CharField()
    ACCOUNT     = CharField()
    DEPT_NAME   = CharField()

    def __str__(self):
        return str(self.__dict__)
