'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''
####Add tables that are referenced via foreign key first

#############################
# USERS
#############################
from app.models.user import User
users = [
             {
             "username": "heggens",
             "FIRST_NAME":"Scott",
             "LAST_NAME": "Heggen",
             "isLaborAdmin": True
             },
            {
                "username": "pearcej",
                "FIRST_NAME":"Jan",
                "LAST_NAME": "Pearce",
                "isLaborAdmin": False
            }
        ]
User.insert_many(users).on_conflict_replace().execute()
print("users added")

#############################
# Students (TRACY)
#############################
from app.models.Tracy.studata import STUDATA

students = [
<<<<<<< HEAD
    {
    "PIDM":"1",
	"ID":"B00730361",
	"FIRST_NAME":"Ela",
    "LAST_NAME":"Jam",
	"CLASS_LEVEL":"Junior",
	"ACADEMIC_FOCUS":"Computer Science",
	"MAJOR":"Computer Science",
	"PROBATION":"0",
	"ADVISOR":"Jan Pearce",
	"STU_EMAIL":"jamalie@berea.edu",
	"STU_CPO":"718",
	"LAST_POSN":"Media Technician",
	"LAST_SUP_PIDM":"7"
    },
    {
    "PIDM":"2",
	"ID":"B00730362",
	"FIRST_NAME":"May",
    "LAST_NAME":"Jue",
	"CLASS_LEVEL":"Junior",
	"ACADEMIC_FOCUS":"Computer Science",
	"MAJOR":"Computer Science",
	"PROBATION":"0",
	"ADVISOR":"Jan Pearce",
	"STU_EMAIL":"jamalie@berea.edu",
	"STU_CPO":"718",
	"LAST_POSN":"Media Technician",
	"LAST_SUP_PIDM":"7"
    },
    {
    "PIDM":"3",
	"ID":"B00730363",
	"FIRST_NAME":"Hailey",
    "LAST_NAME":"Barnett",
	"CLASS_LEVEL":"Junior",
	"ACADEMIC_FOCUS":"Computer Science",
	"MAJOR":"Computer Science",
	"PROBATION":"0",
	"ADVISOR":"Jan Pearce",
	"STU_EMAIL":"jamalie@berea.edu",
	"STU_CPO":"718",
	"LAST_POSN":"Media Technician",
	"LAST_SUP_PIDM":"7"
    }
=======
                {
                "PIDM":"1",
                "ID":"B00730361",
                "FIRST_NAME":"Elaheh",
                "LAST_NAME":"Jamali",
                "CLASS_LEVEL":"Junior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Jan Pearce",
                "STU_EMAIL":"jamalie@berea.edu",
                "STU_CPO":"718",
                "LAST_POSN":"Media Technician",
                "LAST_SUP_PIDM":"7"
                }
>>>>>>> 7e5f7dab2e9f37fa1d2ffde8257b2d1991801312
]
STUDATA.insert_many(students).on_conflict_replace().execute()
print("students(TRACY) added")
from app.models.student import Student
Student.insert_many(students).on_conflict_replace().execute()
print("students(LSF) added")

#############################
# Positions (TRACY)
#############################

from app.models.Tracy.stuposn import STUPOSN

positions = [
                {
                "POSN_CODE": "S61406, S61407",
                "POSN_TITLE": "Student Programmer",
                "WLS": "1 - Entry Level",
                "ORG" : "2114",
                "ACCOUNT":"123456",
                "DEPT_NAME":"Computer Science"
                },
                {
                "POSN_CODE": "S61419",
                "POSN_TITLE": "TA",
                "WLS": "1 - Entry Level",
                "ORG" : "2115",
                "ACCOUNT":"123455",
                "DEPT_NAME":"Mathematics"
                }
]
STUPOSN.insert_many(positions).on_conflict_replace().execute()

print("positions (TRACY) added")

#############################
# TRACY Staff
#############################
from app.models.Tracy.stustaff import STUSTAFF

staffs = [
            {
            "PIDM":"heggens",
            "ID": "B12361006",
            "FIRST_NAME":"Scott",
            "LAST_NAME" : "Heggen",
            "EMAIL"  :"heggens@berea.edu",
            "CPO":"6300",
            "ORG":"Berea College",
            "DEPT_NAME": "CS"
            }
        ]
STUSTAFF.insert_many(staffs).on_conflict_replace().execute()
print("staff added")

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
            },
            {
            "termCode":"201812",
            "termName" :"Summer 2018",
            "termStart":"2018-01-10", #YYYY-MM-DD format.#FIXME: I know this isnt right but idk what the term code above reflects. (ay, spring, etc)
            "termEnd":"2018-05-10",
            "termState":"open",
            },
            {
            "termCode":"201912",
            "termName" :"Summer 2019",
            "termStart":"2018-01-10", #YYYY-MM-DD format.#FIXME: I know this isnt right but idk what the term code above reflects. (ay, spring, etc)
            "termEnd":"2018-05-10",
            "termState":"closed",
            }
        ]
Term.insert_many(terms).on_conflict_replace().execute()
print("terms added")

#############################
# Staff
#############################
from app.models.Tracy.stustaff import STUSTAFF

staffs = [
            {
            "PIDM":"heggens",
            "ID": "B12361006",
            "FIRST_NAME":"Scott",
            "LAST_NAME" : "Heggen",
            "EMAIL"  :"heggens@berea.edu",
            "CPO":"6300",
            "ORG":"Berea College",
            "DEPT_NAME": "CS"
            }
        ]
STUSTAFF.insert_many(staffs).on_conflict_replace().execute()

#############################
# Department
#############################
from app.models.department import Department
depts = [
            {"departmentID":1,
            "DEPT_NAME":"Computer Science",
            "ACCOUNT":"1234",
            "ORG":"4321",
            "departmentCompliance":"True"
            },
            {"departmentID":2,
            "DEPT_NAME":"Mathematics",
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
print("status added")

#############################
# Labor Status Forms
#############################
from app.models.laborStatusForm import LaborStatusForm
from app.models.student import Student
#primary/secondary supervisors are foreign keys to user table
lsfs = [
<<<<<<< HEAD
    {
    "laborStatusFormID": 1,
    "termCode": Term.get(Term.termCode == "201612"),
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
    "primarySupervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"1",
    "POSN_TITLE":"Dummy boi",
    "POSN_CODE":"S12345",
    "startDate": "1/2/3",
    "endDate": "3/2/1"
    },
    {
    "laborStatusFormID": 2,
    "termCode": Term.get(Term.termCode == "201712"),
    "studentSupervisee": Student.get(Student.ID == "B00730362"),
    "primarySupervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "secondary",
    "WLS":"2",
    "POSN_TITLE":"CS TAs",
    "POSN_CODE":"S61419",
    "weeklyHours": 5,
    "startDate": "1/2/3",
    "endDate": "3/2/1"
    },
    {
    "laborStatusFormID": 3,
    "termCode": Term.get(Term.termCode == "201812"),
    "studentSupervisee": Student.get(Student.ID == "B00730363"),
    "primarySupervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "",
    "WLS":"2",
    "POSN_TITLE":"CS TA",
    "POSN_CODE":"S61419",
    "contractHours": 120,
    "startDate": "1/2/3",
    "endDate": "3/2/1"
    }
]
=======
            {
            "laborStatusFormID": 1,
            "termCode": Term.get(Term.termCode == "201612"),
            "studentSupervisee": Student.get(Student.ID == "B00730361"),
            "primarySupervisor": User.get(User.username == "heggens"),
            "department": Department.get(Department.DEPT_NAME == "Computer Science"),
            "jobType": "Primary",
            "WLS":"1",
            "POSN_TITLE":"Dummy boi",
            "POSN_CODE":"S12345",
            "startDate": "1/2/3",
            "endDate": "3/2/1"
            },
            {
            "laborStatusFormID": 2,
            "termCode": Term.get(Term.termCode == "201712"),
            "studentSupervisee": Student.get(Student.ID == "B00730361"),
            "primarySupervisor": User.get(User.username == "heggens"),
            "department": Department.get(Department.DEPT_NAME == "Mathematics"),
            "jobType": "secondary",
            "WLS":"2",
            "POSN_TITLE":"CS TA",
            "POSN_CODE":"S61419",
            "weeklyHours": 5,
            "startDate": "1/2/3",
            "endDate": "3/2/1"
            },
            {
            "laborStatusFormID": 3,
            "termCode": Term.get(Term.termCode == "201812"),
            "studentSupervisee": Student.get(Student.ID == "B00730361"),
            "primarySupervisor": User.get(User.username == "heggens"),
            "department": Department.get(Department.DEPT_NAME == "Mathematics"),
            "jobType": "",
            "WLS":"2",
            "POSN_TITLE":"CS TA",
            "POSN_CODE":"S61419",
            "contractHours": 120,
            "startDate": "1/2/3",
            "endDate": "3/2/1"
            }
        ]
>>>>>>> 7e5f7dab2e9f37fa1d2ffde8257b2d1991801312
LaborStatusForm.insert_many(lsfs).on_conflict_replace().execute()
print("LSF added")

#############################
# Labor Release Forms
#############################
from app.models.laborReleaseForm import LaborReleaseForm
lrfs=[
    {
        "laborReleaseFormID":1,
        "conditionAtRelease":"Satisfactory",
        "releaseDate":"1/2/3",
        "reasonForRelease":"Taking a leave"
    }
]
LaborReleaseForm.insert_many(lrfs).on_conflict_replace().execute()
print("Lrf added")

#############################
# Modified Form
#############################
from app.models.modifiedForm import ModifiedForm
modforms = [
                {
                "modifiedFormID":1,
                "fieldModified":"Term",
                "oldValue":"201612",
                "newValue":"201712",
                "effectiveDate":"1/2/3"
                }
            ]
ModifiedForm.insert_many(modforms).on_conflict_replace().execute()
print("modforms added")

#############################
# Overload form
#############################
#insert dummy overload case here


#############################
# Form History
#############################
#insert form history cases here



#############################
#emailtemplates
#############################
from app.models.emailTemplate import EmailTemplate
emailtemps= [
                {
                "emailTemplateID":"1",
                "purpose":"Labor Status Form Received",
                "subject":"Heres a subject",
                "body":"body yo",
                "audience":"students"
                }
            ]
EmailTemplate.insert_many(emailtemps).on_conflict_replace().execute()
print("emailtemplates added")


print("Dummy data added")
