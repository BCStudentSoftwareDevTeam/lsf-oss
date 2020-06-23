#THIS IS A TRACY FILE! NO TOUCHY!
from app.models.Tracy import db


class STUSTAFF(db.Model):
    __tablename__ = "stustaff"

    PIDM        = db.Column(db.Integer, primary_key=True)           # Unique random ID
    ID          = db.Column(db.String) # B-number
    FIRST_NAME  = db.Column(db.String)
    LAST_NAME   = db.Column(db.String)
    EMAIL       = db.Column(db.String)
    CPO         = db.Column(db.String)
    ORG         = db.Column(db.String)
    DEPT_NAME   = db.Column(db.String)

    def __str__(self):
        return str(self.__dict__)
