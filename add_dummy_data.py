'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''
####Add tables that are referenced via foreign key first

#############################
# USERS
#############################
from datetime import *


# users = [
#              {
#              "PIDM":1,
#              "username": "heggens",
#              "FIRST_NAME":"Scott",
#              "LAST_NAME": "Heggen",
#              "isLaborAdmin": True
#              },
#             {
#             "PIDM":2,
#             "username": "pearcej",
#             "FIRST_NAME":"Jan",
#             "LAST_NAME": "Pearce",
#             "isLaborAdmin": False
#             }
#         ]
# User.insert_many(users).on_conflict_replace().execute()
# print("users added")

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
                {"PIDM":"2",
                "ID":"B00841417",
                "FIRST_NAME":"Alex",
                "LAST_NAME":"Bryant",
                "CLASS_LEVEL":"Senior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Scott Heggen",
                "STU_EMAIL":"bryantal@berea.edu",
                "STU_CPO":"212",
                "LAST_POSN":"Student Manager",
                "LAST_SUP_PIDM":"7"
                },
                {
                "PIDM":"3",
                "ID":"B00734292",
                "FIRST_NAME":"Guillermo",
                "LAST_NAME":"Cruz",
                "CLASS_LEVEL":"Junior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Jan Pearce",
                "STU_EMAIL":"cruzg@berea.edu",
                "STU_CPO":"300",
                "LAST_POSN":"TA",
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
                },
                {
                "ID":"B00841417",
                "FIRST_NAME":"Alex",
                "LAST_NAME":"Bryant",
                "CLASS_LEVEL":"Senior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Scott Heggen",
                "STU_EMAIL":"bryantal@berea.edu",
                "STU_CPO":"212",
                "LAST_POSN":"Student Manager",
                "LAST_SUP_PIDM":"7"
                },
                {
                "ID":"B00734292",
                "FIRST_NAME":"Guillermo",
                "LAST_NAME":"Cruz",
                "CLASS_LEVEL":"Junior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Jan Pearce",
                "STU_EMAIL":"cruzg@berea.edu",
                "STU_CPO":"300",
                "LAST_POSN":"TA",
                "LAST_SUP_PIDM":"7"
                },
                {
                "ID":"B00711232",
                "FIRST_NAME":"May",
                "LAST_NAME":"Jue",
                "CLASS_LEVEL":"Junior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Jan Pearce",
                "STU_EMAIL":"juem@berea.edu",
                "STU_CPO":"123",
                "LAST_POSN":"TA",
                "LAST_SUP_PIDM":"7"
                },
                {
                "ID":"B00734511",
                "FIRST_NAME":"Hila",
                "LAST_NAME":"Manalai",
                "CLASS_LEVEL":"Junior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Jan Pearce",
                "STU_EMAIL":"manalaih@berea.edu",
                "STU_CPO":"224",
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
            "DEPT_NAME":"Computer Science"
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
from app.models.user import User

staffs = [
            {
            "ID": "B12361006",
            "FIRST_NAME":"Scott",
            "LAST_NAME" : "Heggen",
            "EMAIL"  :"heggens@berea.edu",
            "CPO":"6300",
            "ORG":"2141",
            "DEPT_NAME": "Biology"
            },

            {
            "ID": "B12365892",
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"2142",
            "DEPT_NAME": "Computer Science"
            },

            {
            "ID": "B1236236",
            "FIRST_NAME":"Mario",
            "LAST_NAME" : "Nakazawa",
            "EMAIL"  :"nakazawam@berea.edu",
            "CPO":"6302",
            "ORG":"2143",
            "DEPT_NAME": "Mathematics"
            },

            {
            "ID": "B1236236",
            "FIRST_NAME":"Matt",
            "LAST_NAME" : "Jadud",
            "EMAIL"  :"jadudm@berea.edu",
            "CPO":"6303",
            "ORG":"2144",
            "DEPT_NAME": "Geology"
            }


        ]
stustaff = STUSTAFF.insert_many(staffs).on_conflict_replace().execute()
print(stustaff)

def insert_to_users(staffs):
    for sta in staffs[0:3]: #insert staff members into stustaff
        u = User()
        u.PIDM = sta.PIDM
        u.FIRST_NAME = sta.FIRST_NAME
        u.LAST_NAME = sta.LAST_NAME
        u.username = sta.EMAIL.split("@")[0]
        u.EMAIL = sta.EMAIL
        u.CPO = sta.CPO
        u.ORG = sta.ORG
        u.DEPT_NAME = sta.DEPT_NAME
        u.save()
        # ...

insert_to_users(STUSTAFF.select())


#############################
# Terms
#############################
from app.models.term import Term
import datetime
from datetime import date
terms = [
        ##############################
        #        2019-2020
        #############################
    {
    "termCode":"202111",
    "termName" :"Fall 2021",
    "termStart":datetime.date(2021, 8, 20),
    "termEnd": datetime.date(2021, 12, 15)
    },
    {
    "termCode":"202011",
    "termName" :"Fall 2020",
    "termStart":datetime.date(2020, 8, 20),
    "termEnd": datetime.date(2020, 12, 15)
    },
    {
    "termCode":"202012",
    "termName" :"Spring 2021",
    "termStart":datetime.date(2021, 1, 4),
    "termEnd": datetime.date(2021, 5, 5)
    },
    {
    "termCode":"201911",
    "termName" :"Fall 2019",
    "termStart":datetime.date(2019, 8, 20),
    "termEnd": datetime.date(2019, 12, 15)
    },
    {
    "termCode":"201912",
    "termName" :"Spring 2020",
    "termStart":datetime.date(2020, 1, 4),
    "termEnd": datetime.date(2020, 5, 5)
    },
    {
    "termCode":"201901",
    "termName" :"Thanksgiving 2019",
    "termStart":datetime.date(2019, 11, 27),
    "termEnd": datetime.date(2019, 12, 1)
    },
    {
    "termCode":"201902",
    "termName" :"Christmas 2019",
    "termStart":datetime.date(2019, 12, 14),
    "termEnd": datetime.date(2020, 1, 3)
    },
    {
    "termCode":"201903",
    "termName" :"Spring Break 2020",
    "termStart":datetime.date(2020, 4, 12),
    "termEnd": datetime.date(2020, 4, 19)
    },

    {
    "termCode":"201913",
    "termName" :"Summer 2020",
    "termStart":datetime.date(2020, 5, 4),
    "termEnd": datetime.date(2020, 8, 16)
    },

    {
    "termCode":"201900",
    "termName" :"AY 2019-2020",
    "termStart":datetime.date(2019, 8, 16),
    "termEnd": datetime.date(2020, 5, 4)
    },
    ##############################
    #        2018-2019
    #############################
    {
        "termCode":"201801",
        "termName" :"Thanksgiving Break 2018",
        "termStart":datetime.date(2018, 11, 27),
        "termEnd": datetime.date(2018, 12, 1)
        },
    {
        "termCode":"201802",
        "termName" :"Christmas Break 2018",
        "termStart":datetime.date(2018, 12, 16),
        "termEnd": datetime.date(2019, 1, 3)
        },
    {
        "termCode":"201803",
        "termName" :"Spring Break 2019",
        "termStart":datetime.date(2019, 3, 7),
        "termEnd": datetime.date(2019, 3, 14)
        },
    {
        "termCode":"201813",
        "termName" :"Summer 2019",
        "termStart":datetime.date(2019, 5, 4),
        "termEnd": datetime.date(2019, 8, 9)
        },
    {
        "termCode": "201811",
        "termName" :"Fall 2018",
        "termStart":datetime.date(2018, 8, 20),
        "termEnd": datetime.date(2018, 12, 15)
        },
    {
        "termCode":"201812",
        "termName" :"Spring 2019",
        "termStart":datetime.date(2019, 1, 4),
        "termEnd": datetime.date(2019, 5, 5)
        },
    {
        "termCode":"201800",
        "termName" :"AY 2018-2019",
        "termStart":datetime.date(2018, 8, 20),
        "termEnd": datetime.date(2019, 5, 4)
        },
    ##############################
    #        2017-2018
    #############################
    {
    "termCode":"201701",
    "termName" :"Thanksgiving Break 2017",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10)
    },
    {
    "termCode":"201702",
    "termName" :"Christmas Break 2017",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10)
    },
    {
    "termCode":"201703",
    "termName" :"Spring Break 2018",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10)
    },
    {
    "termCode":"201713",
    "termName" :"Summer 2018",
    "termStart":datetime.date(2018, 1, 10),
    "termEnd": datetime.date(2018, 5, 10)
    },
    {
    "termCode": "201711",
    "termName" :"Fall 2017",
    "termStart":datetime.date(2017, 1, 10),
    "termEnd": datetime.date(2017, 5, 10)
    },
    {
    "termCode":"201712",
    "termName" :"Spring 2018",
    "termStart":datetime.date(2018, 4, 14),
    "termEnd": datetime.date(2018, 4, 21)
    },
    {
    "termCode":"201700",
    "termName" :"AY 2017-2018",
    "termStart": datetime.date(2017, 8, 17),
    "termEnd": datetime.date(2018, 5, 4)
    },
    ##############################
    #        2017-2018
    #############################
    {
    "termCode":"201612",
    "termName":"Spring 2017",
    "termStart":datetime.date(2017, 1, 7),
    "termEnd":datetime.date(2017, 5, 4)
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
            "PIDM":1,
            "ID": "B12361006",
            "FIRST_NAME":"Scott",
            "LAST_NAME" : "Heggen",
            "EMAIL"  :"heggens@berea.edu",
            "CPO":"6300",
            "ORG":"Berea College",
            "DEPT_NAME": "CS"
            },

            {
            "PIDM":2,
            "ID": "B12365892",
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"Berea College",
            "DEPT_NAME": "CS"
            },

            {
            "PIDM":3,
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
            },
            {
            "DEPT_NAME":"Biology",
            "ACCOUNT":"9101",
            "ORG":"1019",
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
            },
            {"statusName":"Approved Reluctantly"
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
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"1",
    "POSN_TITLE":"Student Programmer",
    "POSN_CODE":"S61407",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2019,8,20),
    "endDate": datetime.date(2019,12,15)
    },
    {
    "termCode": Term.get(Term.termCode == "201912"),
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"1",
    "POSN_TITLE":"Student Programmer",
    "POSN_CODE":"S61407",
    "weeklyHours": 5,
    "contractHours": None,
    "startDate": datetime.date(2020,1,5),
    "endDate": datetime.date(2020,5,4)
    },
    {
    "termCode": Term.get(Term.termCode == "201913"),
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"Student Programmer",
    "POSN_CODE":"S1407",
    "weeklyHours": None,
    "contractHours": 120,
    "startDate": datetime.date(2020,5,4),
    "endDate": datetime.date(2020,8,9)
    },
    {
    "termCode": Term.get(Term.termCode == "201901"),
    "studentSupervisee": Student.get(Student.ID == "B00730361"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"Student Programmer",
    "POSN_CODE":"S1407",
    "weeklyHours": None,
    "contractHours": 30,
    "startDate": datetime.date(2020,11,25),
    "endDate": datetime.date(2020,11,30)
    },
    {
    "termCode": Term.get(Term.termCode == "201911"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 5,
    "contractHours": None,
    "startDate": datetime.date(2019,8,20),
    "endDate": datetime.date(2019,12,15)
    },
    {
    "termCode": Term.get(Term.termCode == "201912"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2020,1,5),
    "endDate": datetime.date(2020,5,4)
    },
    {
    "termCode": Term.get(Term.termCode == "201913"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": None,
    "contractHours": 120,
    "startDate": datetime.date(2020,5,4),
    "endDate": datetime.date(2020,8,9)
    },
    {
    "termCode": Term.get(Term.termCode == "201901"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": None,
    "contractHours": 30,
    "startDate": datetime.date(2020,11,25),
    "endDate": datetime.date(2020,11,30)
    },
    {
    "termCode": Term.get(Term.termCode == "201911"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2019,8,20),
    "endDate": datetime.date(2019,12,14)
    },
    {
    "termCode": Term.get(Term.termCode == "201912"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2020,1,5),
    "endDate": datetime.date(2020,5,4)
    },
    {
    "termCode": Term.get(Term.termCode == "201913"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": None,
    "contractHours": 120,
    "startDate": datetime.date(2020,5,20),
    "endDate": datetime.date(2020,8,9)
    },
    {
    "termCode": Term.get(Term.termCode == "201901"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": None,
    "contractHours": 20,
    "startDate": datetime.date(2020,11,25),
    "endDate": datetime.date(2020,11,29)
    },
    # {
    # "termCode": Term.get(Term.termCode == "201811"),
    # "studentSupervisee": Student.get(Student.ID == "B00734511"),
    # "supervisor": User.get(User.PIDM == 1),
    # "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    # "jobType": "Primary",
    # "WLS":"1",
    # "POSN_TITLE":"Student Programmer",
    # "POSN_CODE":"S61407",
    # "weeklyHours": 10,
    # "contractHours": None,
    # "startDate": datetime.date(2019,8,20),
    # "endDate": datetime.date(2019,12,15)
    # },
    # {
    # "termCode": Term.get(Term.termCode == "201811"),
    # "studentSupervisee": Student.get(Student.ID == "B00711232"),
    # "supervisor": User.get(User.PIDM == 1),
    # "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    # "jobType": "Primary",
    # "WLS":"1",
    # "POSN_TITLE":"Student Programmer",
    # "POSN_CODE":"S61407",
    # "weeklyHours": 10,
    # "contractHours": None,
    # "startDate": datetime.date(2019,8,20),
    # "endDate": datetime.date(2019,12,15)
    # },
    {
    "termCode": Term.get(Term.termCode == "202011"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2020,1,5),
    "endDate": datetime.date(2020,5,4)
    },
    {
    "termCode": Term.get(Term.termCode == "202011"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2020,1,5),
    "endDate": datetime.date(2020,5,4)
    },
    {
    "termCode": Term.get(Term.termCode == "202012"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2021,2,10),
    "endDate": datetime.date(2021,5,20)
    },
    {
    "termCode": Term.get(Term.termCode == "202012"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 5,
    "contractHours": None,
    "startDate": datetime.date(2021,2,25),
    "endDate": datetime.date(2021,5,22)
    },
    {
    "termCode": Term.get(Term.termCode == "202111"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2021,1,5),
    "endDate": datetime.date(2021,5,5)
    },
    {
    "termCode": Term.get(Term.termCode == "202111"),
    "studentSupervisee": Student.get(Student.ID == "B00841417"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Computer Science"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61419",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2021,1,12),
    "endDate": datetime.date(2021,5,5)
    },
    {
    "termCode": Term.get(Term.termCode == "201711"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Secondary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2017,8,25),
    "endDate": datetime.date(2017,12,14)
    },
    {
    "termCode": Term.get(Term.termCode == "201811"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2018,8,25),
    "endDate": datetime.date(2018,12,14)
    },
    {
    "termCode": Term.get(Term.termCode == "201712"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": 20,
    "contractHours": None,
    "startDate": datetime.date(2018,1,7),
    "endDate": datetime.date(2018,5,4)
    },
    {
    "termCode": Term.get(Term.termCode == "201612"),
    "studentSupervisee": Student.get(Student.ID == "B00734292"),
    "supervisor": User.get(User.PIDM == 1),
    "department": Department.get(Department.DEPT_NAME == "Biology"),
    "jobType": "Primary",
    "WLS":"2",
    "POSN_TITLE":"TA",
    "POSN_CODE":"S61420",
    "weeklyHours": 10,
    "contractHours": None,
    "startDate": datetime.date(2017,1,7),
    "endDate": datetime.date(2017,5,4)
    }
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
        "releaseDate":"2020/6/5",
        "reasonForRelease":"It is just not working really, I wish I could keep her, but I cannot because my family needs me in my life and I need them."
    },
    {
        "conditionAtRelease":"Satisfactory",
        "releaseDate":"2020/6/5",
        "reasonForRelease":"They just need to be released."
    },
    {
        "conditionAtRelease":"Satisfactory",
        "releaseDate":"2020/6/5",
        "reasonForRelease":"He wants to see his family."
    },
    {
        "conditionAtRelease":"Unsatisfactory",
        "releaseDate":"2017/2/10",
        "reasonForRelease":"He STOLE fizzy lifting drinks."
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
                "effectiveDate":"2020/6/8"
                },
                {
                "fieldModified":"Hours",
                "oldValue":"5",
                "newValue":"10",
                "effectiveDate":"2020/6/8"
                },
                {
                "fieldModified":"Hours",
                "oldValue":"30",
                "newValue":"25",
                "effectiveDate":"2020/6/8"
                },
                {
                "fieldModified":"Hours",
                "oldValue":"20",
                "newValue":"25",
                "effectiveDate":"2020/6/8"
                },
                {
                "fieldModified":"Hours",
                "oldValue":"5",
                "newValue":"10",
                "effectiveDate":"2020/6/8"
                },
                {
                "fieldModified":"Hours",
                "oldValue":"5",
                "newValue":"10",
                "effectiveDate":"2017/9/15"
                },
                {
                "fieldModified":"Hours",
                "oldValue":"5",
                "newValue":"10",
                "effectiveDate":"2018/9/15"
                }
            ]
ModifiedForm.insert_many(modforms).on_conflict_replace().execute()
print("modforms added")

#############################
# Overload form
#############################
from app.models.overloadForm import OverloadForm
over = [
        {"overloadReason":"Getting a second position."},
        {"overloadReason":"Needs to have overload. He is good overload."},
        {"overloadReason":"We didn't want to, but we are doing it anyway."},
        {"overloadReason":"Another 10 hour form."},
        {"overloadReason":"Modifying 5 hour form to 10 hour form."},
        {"overloadReason":"We want to deny this."},
        {"overloadReason":"We are denying this, yes."},
        {"overloadReason":"Denied as well."}
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
            "createdBy": User.get(User.PIDM == 1),
            "createdDate": datetime.date(2019, 8, 20),
            "reviewedDate": None,
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Pending"),
            "rejectReason": None
        },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 2),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.PIDM == 1),
            "createdDate": datetime.date(2020, 1, 5),
            "reviewedDate": datetime.date(2020, 5, 4),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
        {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 2),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 1),
            "createdBy": User.get(User.PIDM == 1),
            "createdDate": datetime.date(2020, 1, 7),
            "reviewedDate": datetime.date(2020, 5, 5),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
           {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 3),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.PIDM == 1),
            "createdDate": datetime.date(2020, 5, 4),
            "reviewedDate": datetime.date(2020, 5, 7),
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
            "createdBy": User.get(User.PIDM == 1),
            "createdDate": datetime.date(2020, 6, 5),
            "reviewedDate": datetime.date(2020, 6, 8),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
           {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 4),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
            "releaseForm": None,
            "modifiedForm": None,
            "overloadForm": None,
            "createdBy": User.get(User.PIDM == 1),
            "createdDate": datetime.date(2020, 6, 5),
            "reviewedDate": datetime.date(2020, 6, 8),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
           {
            "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 4),
            "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
            "releaseForm": None,
            "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 1),
            "overloadForm": None,
            "createdBy": User.get(User.PIDM == 1),
            "createdDate": datetime.date(2020, 6, 9),
            "reviewedDate": datetime.date(2020, 6, 10),
            "reviewedBy": None,
            "status": Status.get(Status.statusName == "Approved"),
            "rejectReason": None
           },
           {
           "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 5),
           "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
           "releaseForm": None,
           "modifiedForm": None,
           "overloadForm": None,
           "createdBy": User.get(User.PIDM == 1),
           "createdDate": datetime.date(2019, 8, 20),
           "reviewedDate": datetime.date(2019, 12, 14),
           "reviewedBy": None,
           "status": Status.get(Status.statusName == "Approved"),
           "rejectReason": None
            },
             {
              "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 5),
              "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
              "releaseForm": None,
              "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 2),
              "overloadForm": None,
              "createdBy": User.get(User.PIDM == 1),
              "createdDate": datetime.date(2019, 9, 5),
              "reviewedDate": None,
              "reviewedBy": None,
              "status": Status.get(Status.statusName == "Pending"),
              "rejectReason": None
             },
             {
             "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 6),
             "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
             "releaseForm": None,
             "modifiedForm": None,
             "overloadForm": None,
             "createdBy": User.get(User.PIDM == 1),
             "createdDate": datetime.date(2020, 1, 5),
             "reviewedDate": datetime.date(2020, 5, 4),
             "reviewedBy": None,
             "status": Status.get(Status.statusName == "Pending"),
             "rejectReason": None
                },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 6),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 2),
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2020, 5, 10),
                "reviewedDate": datetime.date(2020, 5, 15),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Pending"),
                "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 7),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 5, 4),
                 "reviewedDate": datetime.date(2020, 5, 7),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 7),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Release Form"),
                 "releaseForm": LaborReleaseForm.get(LaborReleaseForm.laborReleaseFormID == 2),
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 6, 5),
                 "reviewedDate": None,
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Pending"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 8),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 11, 24),
                 "reviewedDate": datetime.date(2020, 11, 25),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 8),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
                 "releaseForm": None,
                 "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 3),
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 11, 27),
                 "reviewedDate": None,
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Pending"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 9),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2019, 8, 20),
                 "reviewedDate": datetime.date(2019, 8, 23),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Denied"),
                 "rejectReason": "He is a great person, but not today."
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 10),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 1, 5),
                 "reviewedDate": datetime.date(2020, 5, 4),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 10),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 3),
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 1, 6),
                 "reviewedDate": datetime.date(2020, 5, 5),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved Reluctantly"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 11),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 5, 20),
                 "reviewedDate": datetime.date(2020, 5, 22),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 11),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Release Form"),
                 "releaseForm": LaborReleaseForm.get(LaborReleaseForm.laborReleaseFormID == 3),
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 5, 24),
                 "reviewedDate": datetime.date(2020, 5, 25),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Denied"),
                 "rejectReason": "We need him too much"
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 12),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 11, 24),
                 "reviewedDate": datetime.date(2020, 11, 25),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved"),
                 "rejectReason": None
                },
                {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 12),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
                 "releaseForm": None,
                 "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 4),
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2020, 11, 27),
                 "reviewedDate": datetime.date(2020, 11, 28),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Denied"),
                 "rejectReason": "Nope"
                },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 13),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": None,
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2020, 8, 20),
                "reviewedDate": datetime.date(2020, 12, 14),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Approved"),
                "rejectReason": None
                 },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 14),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": None,
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2020, 8, 20),
                "reviewedDate": datetime.date(2020, 8, 25),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Pending"),
                "rejectReason": None
                 },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 14),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 4),
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2020, 9, 20),
                "reviewedDate": datetime.date(2020, 9, 25),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Pending"),
                "rejectReason": None
                 },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 15),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": None,
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2021, 2, 20),
                "reviewedDate": datetime.date(2021, 5, 14),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Approved"),
                "rejectReason": None
                 },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 16),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": None,
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2021, 1, 20),
                "reviewedDate": datetime.date(2021, 5, 15),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Approved"),
                "rejectReason": None
                 },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 16),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
                "releaseForm": None,
                "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 5),
                "overloadForm": None,
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2021, 2, 18),
                "reviewedDate": datetime.date(2021, 5, 16),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Pending"),
                "rejectReason": None
                 },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 16),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 5),
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2021, 2, 19),
                "reviewedDate": datetime.date(2021, 5, 17),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Pending"),
                "rejectReason": None
                 },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 17),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                "releaseForm": None,
                "modifiedForm": None,
                "overloadForm": None,
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2021, 1, 5),
                "reviewedDate": None,
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Pending"),
                "rejectReason": None
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 18),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2021, 1, 10),
                 "reviewedDate": None,
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Pending"),
                 "rejectReason": None
                  },
                  {
                  "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 18),
                  "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
                  "releaseForm": None,
                  "modifiedForm": None,
                  "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 6),
                  "createdBy": User.get(User.PIDM == 1),
                  "createdDate": datetime.date(2021, 2, 19),
                  "reviewedDate": datetime.date(2021, 5, 17),
                  "reviewedBy": None,
                  "status": Status.get(Status.statusName == "Denied"),
                  "rejectReason": None
                   },
                  {
                  "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 19),
                  "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                  "releaseForm": None,
                  "modifiedForm": None,
                  "overloadForm": None,
                  "createdBy": User.get(User.PIDM == 1),
                  "createdDate": datetime.date(2017, 8, 25),
                  "reviewedDate": datetime.date(2017, 8, 27),
                  "reviewedBy": None,
                  "status": Status.get(Status.statusName == "Approved"),
                  "rejectReason": None
                   },
                {
                "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 19),
                "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
                "releaseForm": None,
                "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 6),
                "overloadForm": None,
                "createdBy": User.get(User.PIDM == 1),
                "createdDate": datetime.date(2017, 9, 10),
                "reviewedDate": datetime.date(2017, 9, 12),
                "reviewedBy": None,
                "status": Status.get(Status.statusName == "Denied"),
                "rejectReason": "Unnaceptable."
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 19),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 7),
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2017, 9, 11),
                 "reviewedDate": datetime.date(2017, 9, 12),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Denied"),
                 "rejectReason": "You just can't"
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 20),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2018, 8, 25),
                 "reviewedDate": datetime.date(2018, 8, 27),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved"),
                 "rejectReason": None
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 20),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Modified Labor Form"),
                 "releaseForm": None,
                 "modifiedForm": ModifiedForm.get(ModifiedForm.modifiedFormID == 7),
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2018, 9, 10),
                 "reviewedDate": datetime.date(2018, 9, 12),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Denied"),
                 "rejectReason": "You come to me, on my daughter's wedding day, and ask to modify your labor status form?  Denied."
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 21),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2018, 1, 9),
                 "reviewedDate": datetime.date(2018, 1, 12),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Denied"),
                 "rejectReason": "That's too much working"
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 21),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": OverloadForm.get(OverloadForm.overloadFormID == 8),
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2018, 1, 10),
                 "reviewedDate": datetime.date(2018, 1, 13),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Denied"),
                 "rejectReason": "You cannot have this many hours, please seek help."
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 22),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Status Form"),
                 "releaseForm": None,
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2017, 1, 7),
                 "reviewedDate": datetime.date(2017, 1, 8),
                 "reviewedBy": None,
                 "status": Status.get(Status.statusName == "Approved"),
                 "rejectReason": None
                 },
                 {
                 "formID": LaborStatusForm.get(LaborStatusForm.laborStatusFormID == 22),
                 "historyType": HistoryType.get(HistoryType.historyTypeName == "Labor Release Form"),
                 "releaseForm": LaborReleaseForm.get(LaborReleaseForm.laborReleaseFormID == 4),
                 "modifiedForm": None,
                 "overloadForm": None,
                 "createdBy": User.get(User.PIDM == 1),
                 "createdDate": datetime.date(2017, 2, 10),
                 "reviewedDate": datetime.date(2017, 2, 11),
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
                "purpose":"Labor Status Form Submitted For Student",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Student@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is very important. Please take a moment to read carefully and review the information. A Labor Status Form has been submitted for you by <strong>@@Creator@@</strong>. Below is the position information for which you have been hired. If you do not accept the terms of this form, you will have 24 hours to contact the supervisor or the Labor Program Office. If we do not hear from you within 24 hours of this notification, it will be determined that it is accepted and the forms will be processed as submitted.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, your job will be active to allow for time entry in 24 hours. If at that time, you cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p>If you have any further questions or concerns, contact the Labor Program Office at ext. 3611.</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p><strong>Labor Status Form Information:</strong></p>
                            <p>Position Code/Title: <strong>@@Position@@</strong></p>
                            <p>Department Name: <strong>@@Department@@</strong></p>
                            <p>Hours per Week (Total Contracted Hours for Break Periods): <strong>@@Hours@@</strong></p>
                            <p>Begin Date: <strong>@@Date@@</strong></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>Sincerely,</p>
                            <p>Labor Program Office</p>
                            <p>labor_program@berea.edu</p>
                            <p>859-985-3611</p>''',
                "audience":"students"
                },
                {
                "purpose":"Labor Status Form Submitted For Secondary",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong> and <strong>@@Primsupr@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is confirmation that the Labor Program Office has received a Labor Status Form for a secondary position by
                            <strong>@@Supervisor@@</strong> for <strong>@@Student@@</strong>.Please take a moment to read carefully and review the information. Below is the position information for the student you have requested to hire.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student's job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p>If you have any further questions or concerns, contact the Labor Program Office at ext. 3611.</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p><strong>Labor Status Form Information:</strong></p>
                            <p>Student's Name and B-number: <strong>@@Student@@</strong>, <strong>@@StudB@@</strong></p>
                            <p>Position Code/Title: <strong>@@Position@@</strong></p>
                            <p>WLS Level: <strong>@@WLS@@</strong></p>
                            <p>Department Name: <strong>@@Department@@</strong></p>
                            <p>Hours per Week (Total Contracted Hours for Break Periods): <strong>@@Hours@@</strong></p>
                            <p>Begin Date: <strong>@@Date@@</strong></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>Sincerely,</p>
                            <p>Labor Program Office</p>
                            <p>labor_program@berea.edu</p>
                            <p>859-985-3611</p>
                            ''',
                "audience":"supervisor"
                },
                {
                "purpose":"Labor Status Form Submitted For Primary",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is confirmation that the Labor Program Office has received a Labor Status Form
                            <strong>@@Creator@@</strong> for <strong>Student</strong>. Please take a moment to read carefully and review the information Below is the position information for the student you have requested to hire.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student's job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p>If you have any further questions or concerns, contact the Labor Program Office at ext. 3611.</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p><strong>Labor Status Form Information:</strong></p>
                            <p>Student's Name and B-number: <strong>@@Student@@</strong>, <strong>@@StudB@@</strong></p>
                            <p>Position Code/Title: <strong>@@Position@@</strong></p>
                            <p>WLS Level: <strong>@@WLS@@</strong></p>
                            <p>Department Name: <strong>@@Department@@</strong></p>
                            <p>Hours per Week (Total Contracted Hours for Break Periods): <strong>@@Hours@@</strong></p>
                            <p>Begin Date: <strong>@@Date@@</strong></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>Sincerely,</p>
                            <p>Labor Program Office</p>
                            <p>labor_program@berea.edu</p>
                            <p>859-985-3611</p>
                            ''',
                "audience":"supervisor"
                },
                #LSF approved
                {
                "purpose":"Labor Status Form Approved For Student",
                "subject":"Labor Status Form Approved",
                "body":'''<p>Dear <strong>@@Student@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>A Labor This email is very important. Please take a moment to read carefully and review the information. A Labor Release Form previously submitted for you by <strong>@@Student@@</strong> has been <strong>Approved</strong>. You will no longer be able to record time in this position effective of the release date below. If you have concerns, please contact the supervisor or Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> Please allow 24 hours for the position to become active in Tracy (Ultratime). Students should not work until time can be recorded for the position. If at any time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p>If you have any further questions or concerns, contact the Labor Program Office at ext. 3611.</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p><strong>Labor Status Form Information:</strong></p>
                            <p>Student's Name and B-number: <strong>@@Student@@</strong>, <strong>@@StudB@@</strong></p>
                            <p>Position Code/Title: <strong>@@Position@@</strong></p>
                            <p>WLS Level: <strong>@@WLS@@</strong></p>
                            <p>Department Name: <strong>@@Department@@</strong></p>
                            <p>Hours per Week (Total Contracted Hours for Break Periods): <strong>@@Hours@@</strong></p>
                            <p>Begin Date: <strong>@@Date@@</strong></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>Sincerely,</p>
                            <p>Labor Program Office</p>
                            <p>labor_program@berea.edu</p>
                            <p>859-985-3611</p>
                            ''',
                "audience":"supervisor"
                },
                {
                "purpose":"Labor Status Form Approved For Primary",
                "subject":"Labor Status Form Approved",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>A Labor Status Form previously submitted by you for
                            <strong>@@Student@@</strong> has been <strong>Approved</strong>. Below is the position information for the student that you have hired.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> Please allow 24 hours for the position to become active in Tracy (Ultratime). Students should not work until time can be recorded for the position. If at any time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p>If you have any further questions or concerns, contact the Labor Program Office at ext. 3611.</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p><strong>Labor Status Form Information:</strong></p>
                            <p>Student's Name and B-number: <strong>@@Student@@</strong>, <strong>@@StudB@@</strong></p>
                            <p>Position Code/Title: <strong>@@Position@@</strong></p>
                            <p>WLS Level: <strong>@@WLS@@</strong></p>
                            <p>Department Name: <strong>@@Department@@</strong></p>
                            <p>Hours per Week (Total Contracted Hours for Break Periods): <strong>@@Hours@@</strong></p>
                            <p>Begin Date: <strong>@@Date@@</strong></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>Sincerely,</p>
                            <p>Labor Program Office</p>
                            <p>labor_program@berea.edu</p>
                            <p>859-985-3611</p>
                            ''',
                "audience":"supervisor"
                },
                {
                "purpose":"Labor Status Form Approved For Secondary",
                "subject":"Labor Status Form Approved",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                #LSF Rejected
                {
                "purpose":"Labor Status Form Rejected For Student",
                "subject":"Labor Status Form Rejected",
                "body":'''
                            ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Status Form Rejected For Secondary",
                "subject":"Labor Status Form Rejected",
                "body":'''<p>Dear <strong>@@Primsupr@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>A Labor Status Form previously submitted by you for
                            <strong>@@Student@@</strong>,<strong>%%StudB%%</strong> hiring him/her to work in a secondary position has been Denied. This is an informational email to you as the supervisor for the primary labor position.</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p><strong>Labor Status Form Information:</strong></p>
                            <p>Student's Name and B-number: <strong>@@Student@@</strong>, <strong>@@StudB@@</strong></p>
                            <p>Position Code/Title: <strong>@@Position@@</strong></p>
                            <p>WLS Level: <strong>@@WLS@@</strong></p>
                            <p>Department Name: <strong>@@Department@@</strong></p>
                            <p>Hours per Week (Total Contracted Hours for Break Periods): <strong>@@Hours@@</strong></p>
                            <p>Begin Date: <strong>@@Date@@</strong></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>Sincerely,</p>
                            <p>Labor Program Office</p>
                            <p>labor_program@berea.edu</p>
                            <p>859-985-3611</p>
                            ''',
                "audience":"supervisor"
                },
                {
                "purpose":"Labor Status Form Rejected For Primary",
                "subject":"Labor Status Form Rejected",
                "body":'''
                            ''',
                "audience":"student"
                },
                #LSF modified
                {
                "purpose":"Labor Status Form Modified For Student",
                "subject":"Labor Status Form Modified",
                "body":'''
                            ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Status Form Modified For Supervisor",
                "subject":"Labor Status Form Modified",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                #LRF Submitted
                {
                "purpose":"Labor Release Form Submitted For Student",
                "subject":"Labor Release Form Submitted",
                "body":'''
                            ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Release Form Submitted For Supervisor",
                "subject":"Labor Release Form Submitted",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                #LRF approved
                {
                "purpose":"Labor Release Form Approved For Student",
                "subject":"Labor Release Form Approved",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is very important. Please take a moment to read carefully and review the information. A Labor Release Form previously submitted for you by <strong>@@Supervisor@@</strong> has been <strong>Approved</strong>. You will no longer be able to record time in this position effective of the release date below. If you have concerns, please contact the supervisor or Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p>If you have any further questions or concerns, contact the Labor Program Office at ext. 3611.</p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p><strong>Labor Status Form Information:</strong></p>
                            <p>Student's Name and B-number: <strong>@@Student@@</strong>, <strong>@@StudB@@</strong></p>
                            <p>Position Code/Title: <strong>@@Position@@</strong></p>
                            <p>WLS Level: <strong>@@WLS@@</strong></p>
                            <p>Department Name: <strong>@@Department@@</strong></p>
                            <p>Release Date: <strong>@@ReleaseDate@@</strong></p>
                            <p>Reason for Release:: <strong>@@ReleaseReason@@</strong></p>
                            <p>&nbsp;</p>
                            <p>&nbsp;</p>
                            <p>Sincerely,</p>
                            <p>Labor Program Office</p>
                            <p>labor_program@berea.edu</p>
                            <p>859-985-3611</p>
                            ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Release Form Approved For Supervisor",
                "subject":"Labor Release Form Approved",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                #LRF Rejected
                {
                "purpose":"Labor Release Form Rejected For Student",
                "subject":"Labor Release Form Rejected",
                "body":'''
                            ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Release Form Rejected For Supervisor",
                "subject":"Labor Release Form Rejected",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                #LOF
                {
                "purpose":"Labor Overload Form Submitted For Student",
                "subject":"Labor Overload Form Submitted",
                "body":'''
                    <p>Dear <strong>@@Student@@</strong>,</p>
                    <p>&nbsp;</p>
                    <p>Please follow the attached link to verify information needed for the approval of an overload form: <a href="@@link@@">@@link@@</a></p>
                    ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Overload Form Submitted For Supervisor",
                "subject":"Labor Overload Form Submitted",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                {
                "purpose":"Labor Overload Form Approved For Student",
                "subject":"Labor Overload Form Approved",
                "body":'''
                            ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Overload Form Approved For Supervisor",
                "subject":"Labor Overload Form Approved",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                {
                "purpose":"Labor Overload Form Rejected For Student",
                "subject":"Labor Overload Form Rejected",
                "body":'''
                            ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Overload Form Rejected For Supervisor",
                "subject":"Labor Overload Form Rejected",
                "body":'''
                            ''',
                "audience":"supervisor"
                },
                #SASS
                {
                "purpose":"SASS and Financial Aid Office",
                "subject":"Overload Verification",
                "body":'''
                    <p>Please follow the attached link to verify information needed for the approval of an overload form: <a href="@@link@@">@@link@@</a></p>
                            ''',
                "audience":"supervisor"
                }
            ]
EmailTemplate.insert_many(emailtemps).on_conflict_replace().execute()
print("emailtemplates added")

print("Dummy data added")
