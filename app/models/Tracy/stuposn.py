#THIS IS A TRACY FILE! NO TOUCHY!
from app.models.Tracy import db


class STUPOSN(db.Model):
    __tablename__ = "stuposn"

    POSN_CODE   = db.Column(db.String, primary_key=True)           # Unique random ID
    POSN_TITLE  = db.Column(db.String)
    WLS         = db.Column(db.String)
    ORG         = db.Column(db.String)
    ACCOUNT     = db.Column(db.String)
    DEPT_NAME   = db.Column(db.String)

    def __str__(self):
        return str(self.__dict__)
