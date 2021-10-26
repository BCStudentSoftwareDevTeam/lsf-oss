from app.models import *
from app.models.student import Student
from app.models.supervisor import Supervisor
from peewee import CharField
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


# Capitalized fields are originally pulled from tracy
class User(UserMixin, baseModel):
    userID              = PrimaryKeyField()
    student             = ForeignKeyField(Student, null=True)
    supervisor          = ForeignKeyField(Supervisor, null=True)
    username            = CharField(null=False)
    isLaborAdmin        = BooleanField(null=True)
    isFinancialAidAdmin = BooleanField(null=True)
    isSaasAdmin         = BooleanField(null=True)
    email               = CharField(null=True)
    localPassword       = FixedCharField(max_length=128, null=True)

    def __str__(self):
        return str(self.__dict__)

    # For local login only
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    # For local login only
    @password.setter
    def password(self, localLoginPassword):
        self.localPassword = generate_password_hash(localLoginPassword)

    # For local login only
    def verify_password(self, password):
        return check_password_hash(self.localPassword, password)
