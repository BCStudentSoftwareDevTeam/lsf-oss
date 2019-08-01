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

    ##############################
    #        2021-2022
    #############################
    {
    "termCode":"202101",
    "termName" :"Thanksgiving Break 2021",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202102",
    "termName" :"Christmas Break 2021",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202103",
    "termName" :"Spring Break 2022",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202113",
    "termName" :"Summer 2022",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode": "202111",
    "termName" :"Fall 2021",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202112",
    "termName" :"Spring 2022",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202100",
    "termName" :"AY 2021-2022",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    ##############################
    #        2020-2021
    #############################

    {
    "termCode":"202001",
    "termName" :"Thanksgiving Break 2020",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202002",
    "termName" :"Christmas Break 2020",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202003",
    "termName" :"Spring Break 2021",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202013",
    "termName" :"Summer 2021",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode": "202011",
    "termName" :"Fall 2020",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202012",
    "termName" :"Spring 2021",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"202000",
    "termName" :"AY 2020-2021",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
        ##############################
        #        2019-2020
        #############################

    {
    "termCode":"201911",
    "termName" :"Fall 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },

    {
    "termCode":"201912",
    "termName" :"Spring 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201901",
    "termName" :"Thanksgiving 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },

    {
    "termCode":"201902",
    "termName" :"Christmas 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201903",
    "termName" :"Spring Break 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },

    {
    "termCode":"201913",
    "termName" :"Summer 2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },

    {
    "termCode":"201900",
    "termName" :"AY 2019-2020",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    ##############################
    #        2018-2019
    #############################
    {
    "termCode":"201801",
    "termName" :"Thanksgiving Break 2018",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201802",
    "termName" :"Christmas Break 2018",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201803",
    "termName" :"Spring Break 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201813",
    "termName" :"Summer 2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode": "201811",
    "termName" :"Fall 2018",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201812",
    "termName" :"Spring 2019",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201800",
    "termName" :"AY 2018-2019",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    ##############################
    #        2017-2018
    #############################
    {
    "termCode":"201701",
    "termName" :"Thanksgiving Break 2017",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201702",
    "termName" :"Christmas Break 2017",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201703",
    "termName" :"Spring Break 2018",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201713",
    "termName" :"Summer 2018",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
    },
    {
    "termCode": "201711",
    "termName" :"Fall 2017",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201712",
    "termName" :"Spring 2018",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10),
    "termState":"True",
    },
    {
    "termCode":"201700",
    "termName" :"AY 2017-2018",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10),
    "termState":"True",
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
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
    "supervisor": User.get(User.username == "heggens"),
    "department": Department.get(Department.DEPT_NAME == "Mathematics"),
    "jobType": "secondary",
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
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
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
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
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
            "formID": LaborStatusForm.get(LaborStatusForm.studentSupervisee == "B00730361"),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 5, 17),
            "reviewedDate": None,
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
        },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.studentSupervisee == "B00730361"),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 5, 17),
            "reviewedDate": None,
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.studentSupervisee == "B00730361"),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 5, 17),
            "reviewedDate": None,
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.studentSupervisee == "B00730361"),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.username == "heggens"),
            "createdDate": datetime.date(2019, 5, 17),
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
