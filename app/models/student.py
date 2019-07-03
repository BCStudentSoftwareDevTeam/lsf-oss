from app.models.util import *
from app.models.user import *
#Any foreign keys or other imports

#Note: if you update the model, you will need to update the queries to pull the right attributes you want
class student (baseModel):
    bNumber                         = CharField(primary_key=True)
    firstName                       = CharField()
    lastName                        = CharField()
    email                           = CharField()
    lastSupervisorUsername          = ForeignKeyField(user)
    #Do we need any more infor about past labor supervisor?
    #Any more info about student?? studata.cs has: pidm, last_sup_pidm, and id, but i assume id is bnumber...)
    def __str__(self):
        return str(self.bNumber)

#Queries as helper functions
####FIX ME: these are currently written as if they were in a class. Fix them to work with the student class
def select_all_students(self):
    try:
        students = student.select()
        return students
    except Exception as e:
        print ("select_all_students",e)
        return False

def select_single_student(self, formID):
    try:
      student = student.get(student.bNumber == bNumber)
      return student
    except Exception as e:
      print ("select_single_student",e)
      return False

def insert_student(self, bNumber, firstName, lastName, email, lastSupervisorUsername):
    try:
        student = student(bNumber = bNumber, firstName = firstName, lastName = lastName,
                            email = email, lastSupervisorUsername = lastSupervisorUsername)
        student.save()
        return student
    except Exception as e:
        print ("insert_user",e)
        return e
