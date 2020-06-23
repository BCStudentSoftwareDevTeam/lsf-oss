#THIS IS A TRACY FILE! NO TOUCHY!
from app.models.Tracy import db


class STUDATA(db.Model):
    __tablename__ = "studata"

    PIDM                    = db.Column(db.String, primary_key=True)           # Unique random ID
    ID                      = db.Column(db.String) #B-number
    FIRST_NAME              = db.Column(db.String)
    LAST_NAME               = db.Column(db.String)
    CLASS_LEVEL             = db.Column(db.String)
    ACADEMIC_FOCUS          = db.Column(db.String)
    MAJOR                   = db.Column(db.String)
    PROBATION               = db.Column(db.String)
    ADVISOR                 = db.Column(db.String)
    STU_EMAIL               = db.Column(db.String)
    STU_CPO                 = db.Column(db.String)
    LAST_POSN               = db.Column(db.String)
    LAST_SUP_PIDM           = db.Column(db.String)

    def __str__(self):
        return str(self.__dict__)
