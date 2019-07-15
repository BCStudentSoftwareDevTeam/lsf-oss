'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''
####Add tables that are referenced via foreign key first
#############################
# USERS
#############################
from app.models.user import User
users = [
     # {
     #    "username": "pearcej",
     #    "firstname": "Jan",
     #    "lastname": "Pearce"
     # },
     ###NEW FORMAT:###
     {
     "username": "heggens",
     "FIRST_NAME":"Scott",
     "LAST_NAME": "Heggen",
     # "bNumber": "B01234567"
     }
    ]
User.insert_many(users).on_conflict_replace().execute()
print("users added")
#############################
# Students
#############################
from app.models.student import Student
students = [
    {
    "PIDM":"1",# Unique random ID
    "ID":"B012341234",# B-number
    "FIRST_NAME" : "Jose",
    "LAST_NAME":"Garcia",
    "CLASS_LEVEL":"Sophomore",
    "STU_EMAIL":"dummydumdum@berea.edu",
    "STU_CPO":"1234"
    }
]
Student.insert_many(students).on_conflict_replace().execute()
print("students added")
#############################
# Terms
#############################
from app.models.term import Term
terms = [
    {
    "termCode":"201612",
    "termName" :"201612's name",
    "termStart":"2017-01-10", #YYYY-MM-DD format.#FIXME: I know this isnt right but idk what the term code above reflects. (ay, spring, etc)
    "termEnd":"2017-05-10",
    "termState":"open",
    },
    {
    "termCode":"201712",
    "termName" :"201712's name",
    "termStart":"2018-01-10", #YYYY-MM-DD format.#FIXME: I know this isnt right but idk what the term code above reflects. (ay, spring, etc)
    "termEnd":"2018-05-10",
    "termState":"closed",
    }
    #add more term cases here
]
Term.insert_many(terms).on_conflict_replace().execute()
print("terms added")
#############################
# Department
#############################
from app.models.department import Department
depts = [
    {"DEPT_NAME":"Computer Science",
    "ACCOUNT":"1234",
    "ORG":"4321",
    "departmentCompliance":"True"
    },
    {"DEPT_NAME":"Mathematics",
    "ACCOUNT":"5678",
    "ORG":"8765",
    "departmentCompliance":"True"
    }
]
Department.insert_many(depts).on_conflict_replace().execute()
print("departments added")
#############################
# Status
#############################
from app.models.status import Status
stats = [
    {"statusName":"Pending"
    },
    {"statusName":"Approved"
    }
]
Status.insert_many(stats).on_conflict_replace().execute()
print("staats added")
#############################
# Labor Status Forms
#############################
from app.models.laborStatusForm import LaborStatusForm
lsfs = [
    {
    "laborStatusFormID": 1,
    "termCode": Term.get(Term.termCode == "201612"),
    "ID": Student.get(Student.ID == "B012341234"),
    "username": User.get(User.username == "heggens"),
    "DEPT_NAME": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"1",
    "POSN_TITLE":"Dummy boi",
    "POSN_CODE":"S12345",
    "startDate": "1/2/3",
    "endDate": "3/2/1"
    }
]
LaborStatusForm.insert_many(lsfs).on_conflict_replace().execute()
print("LSF added")
#############################
# Labor Release Forms
#############################


#############################
# Modified Form
#############################

#############################
# Overload form
#############################


print("Dummy data added")

#TODO To be continued...
