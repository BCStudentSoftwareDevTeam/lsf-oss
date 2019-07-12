#tracy file
#im not sure if we wil need this file cause of the other student tables but....
from app.models import *
#Any foreign keys or other imports

class Student(baseModel):
    studentUsername             = CharField(primary_key=True)
    studentFirstName            = CharField(null=False)
    studentLastName             = CharField(null=False)
    studentBNumber              = CharField(null=False)
    studentCPO                  = CharField(null=True) #not sure if we will be needing this
    #any other TRACY info...
