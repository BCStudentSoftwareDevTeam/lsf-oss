'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''
####Add tables that are referenced via foreign key first

#############################
# USERS
#############################
from datetime import *

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

studentsTracy = [
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
                }
]
STUDATA.insert_many(studentsTracy).on_conflict_replace().execute()
print("students(TRACY) added")

#############################
# Students
#############################
from app.models.student import Student

students = [
    {
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
    },
    {
	"ID":"B00730364",
	"FIRST_NAME":"Riel",
    "LAST_NAME":"Pursun",
	"CLASS_LEVEL":"Frashman",
	"ACADEMIC_FOCUS":"Computer Science",
	"MAJOR":"Computer Science",
	"PROBATION":"0",
	"ADVISOR":"Jan Pearce",
	"STU_EMAIL":"jamalie@berea.edu",
	"STU_CPO":"718",
	"LAST_POSN":"Media Technician",
	"LAST_SUP_PIDM":"7"
    }

]

Student.insert_many(students).on_conflict_replace().execute()
print("students(LSF) added")

#############################
# Positions (TRACY)
#############################
from app.models.Tracy.stuposn import STUPOSN

positions = [
            {
            "POSN_CODE": "S61407",
            "POSN_TITLE": "Student Programmer",
            "WLS": "1",
            "ORG" : "2114",
            "ACCOUNT":"123456",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61419",
            "POSN_TITLE": "TA",
            "WLS": "1",
            "ORG" : "2115",
            "ACCOUNT":"123455",
            "DEPT_NAME":"Mathematics"
            },
            {
            "POSN_CODE": "S61420",
            "POSN_TITLE": "TA",
            "WLS": "1",
            "ORG" : "2115",
            "ACCOUNT":"123455",
            "DEPT_NAME":"Biology"
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
            },

            {
            "PIDM":"pearcej",
            "ID": "B12365892",
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"Berea College",
            "DEPT_NAME": "CS"
            },

            {
            "PIDM":"nakazawam",
            "ID": "B1236236",
            "FIRST_NAME":"Mario",
            "LAST_NAME" : "Nakazawa",
            "EMAIL"  :"nakazawam@berea.edu",
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
import datetime
from datetime import date

terms = [
    {
    "termCode":"201901",  # termcode for ThanksGiving
    "termName" :"Thanksgiving 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },
    {
    "termCode":"201911",
    "termName" :"Fall 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },

    {
    "termCode":"201912",
    "termName" :"Spring 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },
    {
    "termCode":"201901",
    "termName" :"Thanksgiving 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },
    {
    "termCode":"201900",
    "termName" :"AY 2019-2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },
    {
    "termCode":"201902",
    "termName" :"Christmas 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },
    {
    "termCode":"201903",
    "termName" :"Spring Break 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },
    {
    "termCode":"201912",
    "termName" :"Spring 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
    },
    {
    "termCode":"201913",
    "termName" :"Summer 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"open",
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
            },

            {
            "PIDM":"pearcej",
            "ID": "B12365892",
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"Berea College",
            "DEPT_NAME": "CS"
            },

            {
            "PIDM":"nakazawam",
            "ID": "B1236236",
            "FIRST_NAME":"Mario",
            "LAST_NAME" : "Nakazawa",
            "EMAIL"  :"nakazawam@berea.edu",
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
            {
            "DEPT_NAME":"Computer Science",
            "ACCOUNT":"1234",
            "ORG":"4321",
            "departmentCompliance":"True"
            },
            {
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
            },
            {"statusName":"Denied"
            }
        ]
Status.insert_many(stats).on_conflict_replace().execute()
print("status added")

#############################
# Labor Status Forms
#############################
from app.models.laborStatusForm import LaborStatusForm
from app.models.student import Student
from app.models.department import Department
from app.models.term import Term
import datetime
from datetime import date
lsfs = [

    {
    "termCode": Term.get(Term.termCode == "201911"),
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
    "supervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"1",
    "POSN_TITLE":"Dummy boi",
    "POSN_CODE":"S61406",
    "weeklyHours": 5,
    "contractHours": None,
    "startDate": datetime.date(1,2,3),
    "endDate": datetime.date(3,2,1)
    },
    {
    "termCode": Term.get(Term.termCode == "201912"),
    "studentSupervisee": Student.get(Student.ID == "B00730362"),
    "supervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"CS TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 5,
    "contractHours": None,
    "startDate": datetime.date(1,2,3),
    "endDate": datetime.date(3,2,1)
    },
    {
    "termCode": Term.get(Term.termCode == "201913"),
    "studentSupervisee": Student.get(Student.ID == "B00730363"),
    "supervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "",
    "WLS":"2",
    "POSN_TITLE":"CS TA",
    "POSN_CODE":"S61419",
    "weeklyHours": None,
    "contractHours": 120,
    "startDate": datetime.date(1,2,3),
    "endDate": datetime.date(3,2,1)
    },
    {
    "termCode":"201901",    #ThanksGiving break code
    "studentSupervisee": Student.get(Student.ID == "B00730364"),
    "supervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "",
    "WLS":"2",
    "POSN_TITLE":"Teaching Assistant",
    "POSN_CODE":"S61419",
    "weeklyHours": None,
    "contractHours": 120,
    "startDate": datetime.date(1,2,3),
    "endDate": datetime.date(3,2,1)
    },
    {
    "termCode":"201901",    #ThanksGiving break code
    "studentSupervisee": Student.get(Student.ID == "B00730362"),
    "supervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "",
    "WLS":"2",
    "POSN_TITLE":"Teaching Assistant",
    "POSN_CODE":"S61419",
    "weeklyHours": None,
    "contractHours": 120,
    "startDate": datetime.date(1,5,1),
    "endDate": datetime.date(3,2,5)
    },
    {
    "termCode":"201901",    #ThanksGiving break code
    "studentSupervisee": Student.get(Student.ID == "B00730362"),
    "supervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "",
    "WLS":"2",
    "POSN_TITLE":"Teaching Assistant",
    "POSN_CODE":"S61419",
    "weeklyHours": None,
    "contractHours": 120,
    "startDate": datetime.date(2,5,1),
    "endDate": datetime.date(3,7,5)
    },
]

LaborStatusForm.insert_many(lsfs).on_conflict_replace().execute()
# ls = LaborStatusForm.get(LaborStatusForm.studentSupervisee == "B00730361")
# ls.contractHours = 120
# ls.save()
print("LSF added")
#############################
# Labor Release Forms
#############################
from app.models.laborReleaseForm import LaborReleaseForm
lrfs=[
    {
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
                "fieldModified":"Hours",
                "oldValue":"5",
                "newValue":"10",
                "effectiveDate":"1/2/3"
                },
                {
                "fieldModified":"WLS",
                "oldValue":"1",
                "newValue":"5",
                "effectiveDate":"1/2/3"
                }
            ]
ModifiedForm.insert_many(modforms).on_conflict_replace().execute()
print("modforms added")

#############################
# Overload form
#############################
from app.models.overloadForm import OverloadForm
over = [
        {"overloadReason":"Needed a break"}
        ]
OverloadForm.insert_many(over).on_conflict_replace().execute()
print("Added modified")


#############################
# History Type
#############################
from app.models.historyType import HistoryType
types = [
            {"historyTypeName":"Labor Status Form"
            },
            {"historyTypeName":"Labor Overload Form"
            },
            {"historyTypeName":"Labor Release Form"
            },
            {"historyTypeName":"Modified Labor Form"
            }
        ]
HistoryType.insert_many(types).on_conflict_replace().execute()
print("history types added")

#############################
# Form History
#############################
#insert form history cases here
from app.models.formHistory import FormHistory
import datetime



fh = [  {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 1),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 1, 17),
            "reviewedDate": datetime.date(2019, 1, 20),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
        },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 2),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
            "releaseForm": None,
            "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 1),
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 2, 3),
            "reviewedDate": datetime.date(2019, 2, 15),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 3),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Release Form"),
            "releaseForm": LaborReleaseForm.get(LaborReleaseForm.laborReleaseFormID == 1),
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2020, 3, 10),
            "reviewedDate": datetime.date(2020, 3, 21),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Denied"),
            "rejectReason": None
           },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 4),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 1),
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 6, 17),
            "reviewedDate": None,
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Pending"),
            "rejectReason": None
           },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 4),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 6, 17),
            "reviewedDate": None,
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           }

    ]

FormHistory.insert_many(fh).on_conflict_replace().execute()
print("Form history added")

#############################
#emailtemplates
#############################
from app.models.emailTemplate import EmailTemplate
emailtemps= [
                {
                "purpose":"Labor Status Form Received",
                "subject":"Heres a subject",
                "body":"body yo",
                "audience":"students"
                }
            ]
EmailTemplate.insert_many(emailtemps).on_conflict_replace().execute()
print("emailtemplates added")

print("Dummy data added")
