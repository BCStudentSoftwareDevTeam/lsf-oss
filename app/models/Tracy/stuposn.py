from app.models.Tracy import *


class STUPOSN(baseModel):
    POSN_CODE   = CharField(primary_key=True)
    POSN_TITLE  = CharField(null=True)
    WLS         = CharField(null=True)
    ORG         = CharField(null=True)
    ACCOUNT     = CharField(null=True)
    DEPT_NAME   = CharField(null=True)

    def __str__(self):
        return str(self.__dict__)
