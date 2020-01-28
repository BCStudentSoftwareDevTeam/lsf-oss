'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''
####Add tables that are referenced via foreign key first

from datetime import *

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
                },
                {
                "PIDM":"4",
                "ID":"B00785329",
                "FIRST_NAME":"Kat",
                "LAST_NAME":"Adams",
                "CLASS_LEVEL":"Senior",
                "ACADEMIC_FOCUS":"Computer Science",
                "MAJOR":"Computer Science",
                "PROBATION":"0",
                "ADVISOR":"Scott Heggen",
                "STU_EMAIL":"adamskg@berea.edu",
                "STU_CPO":"420",
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
            "ORG" : "4321",
            "ACCOUNT":"1234",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61408",
            "POSN_TITLE": "Research Associate",
            "WLS": "5",
            "ORG" : "4321",
            "ACCOUNT":"1234",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61419",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "3",
            "ORG" : "4321",
            "ACCOUNT":"1234",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61420",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "5",
            "ORG" : "9102",
            "ACCOUNT":"1020",
            "DEPT_NAME":"Technology and Applied Design"
            },
            {
            "POSN_CODE": "S61421",
            "POSN_TITLE": "TA",
            "WLS": "6",
            "ORG" : "4321",
            "ACCOUNT":"1234",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61427",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "2",
            "ORG" : "5678",
            "ACCOUNT":"8765",
            "DEPT_NAME":"Mathematics"
            },
            {
            "POSN_CODE": "S61430",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "5",
            "ORG" : "1019",
            "ACCOUNT":"9101",
            "DEPT_NAME":"Biology"
            },
            {
            "POSN_CODE": "S61443",
            "POSN_TITLE": "Lab Assistant",
            "WLS": "6",
            "ORG" : "1019",
            "ACCOUNT":"9101",
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

    #TODO: Ask Scott about isLaborAdmin field
            {
            "PIDM":1,
            "ID": "B12361006",
            "FIRST_NAME":"Scott",
            "LAST_NAME" : "Heggen",
            "EMAIL"  :"heggens@berea.edu",
            "CPO":"6300",
            "ORG":"2141",
            "DEPT_NAME": "Biology"

            },

            {
            "PIDM":2,
            "ID": "B12365892",
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"2142",
            "DEPT_NAME": "Computer Science"
            },

            {
            "PIDM":3,
            "ID": "B1236236",
            "FIRST_NAME":"Mario",
            "LAST_NAME" : "Nakazawa",
            "EMAIL"  :"nakazawam@berea.edu",
            "CPO":"6302",
            "ORG":"2143",
            "DEPT_NAME": "Mathematics"
            },

            {
            "PIDM":4,
            "ID": "B1236237",
            "FIRST_NAME":"Megan",
            "LAST_NAME" : "Hoffman",
            "EMAIL"  :"hoffmanm@berea.edu",
            "CPO":"6303",
            "ORG":"2144",
            "DEPT_NAME": "Biology"
            },
            {
            "PIDM":5,
            "ID": "B12365893",
            "FIRST_NAME":"Jasmine",
            "LAST_NAME" : "Jones",
            "EMAIL"  :"jonesj@berea.edu",
            "CPO":"6301",
            "ORG":"2142",
            "DEPT_NAME": "Computer Science"
            }
        ]
stustaff = STUSTAFF.insert_many(staffs).on_conflict_replace().execute()
print(stustaff)
print("staff added")

def insert_to_users(staffs):
    for sta in staffs: #insert staff members into stustaff
        try:
            u = User()
            u.FIRST_NAME = sta.FIRST_NAME
            u.LAST_NAME = sta.LAST_NAME
            u.username = sta.EMAIL.split("@")[0]
            u.EMAIL = sta.EMAIL
            u.CPO = sta.CPO
            u.ORG = sta.ORG
            u.DEPT_NAME = sta.DEPT_NAME
            u.save()
        except Exception as e:
            pass
insert_to_users(STUSTAFF.select())

#############################
# Terms
#############################
from app.models.term import Term
import datetime
from datetime import date
terms = [

        ##############################
        #        2020-2021
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

        ##############################
        #        2019-2020
        #############################
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
    "termStart":datetime.date(2020, 3, 2),
    "termEnd": datetime.date(2020, 3, 8)
    },
    {
    "termCode":"201913",
    "termName" :"Summer 2020",
    "termStart":datetime.date(2020, 5, 10),
    "termEnd": datetime.date(2020, 8, 9)
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
        "termCode":"201800",
        "termName" :"AY 2018-2019",
        "termStart":datetime.date(2018, 8, 20),
        "termEnd": datetime.date(2019, 5, 4)
        },
    ##############################
    #        2017-2018
    #############################
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
            "ORG":"1019",
            "DEPT_NAME": "Biology"
            },

            {
            "PIDM":2,
            "ID": "B12365892",
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"4321",
            "DEPT_NAME": "Computer Science"
            },

            {
            "PIDM":3,
            "ID": "B1236236",
            "FIRST_NAME":"Mario",
            "LAST_NAME" : "Nakazawa",
            "EMAIL"  :"nakazawam@berea.edu",
            "CPO":"6300",
            "ORG":"4321",
            "DEPT_NAME": "Mathematics"
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
            },
            {
            "DEPT_NAME":"Technology and Applied Design",
            "ACCOUNT":"9102",
            "ORG":"1020",
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
]
LaborReleaseForm.insert_many(lrfs).on_conflict_replace().execute()
print("Lrf added")
#############################
# Modified Form
#############################
from app.models.modifiedForm import ModifiedForm
modforms = [
            ]
ModifiedForm.insert_many(modforms).on_conflict_replace().execute()
print("modforms added")

#############################
# Overload form
#############################
from app.models.overloadForm import OverloadForm
'''Overload reason should show the reason why the student believes the need an overload'''
over = [
        ]
OverloadForm.insert_many(over).on_conflict_replace().execute()
print("overload added")

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

fh = [
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
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
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
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
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
                <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
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
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
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
                "purpose":"Labor Overload Form Submitted Notification For Student",
                "subject":"Labor Overload Form Submitted Notification",
                "body":'''
                    <p>Dear <strong>@@Student@@</strong>,</p>
                    <p>&nbsp;</p>
                    <p>This is a confiramtion that you submitted a reason for the overload form requested for you.</p>
                    ''',
                "audience":"student"
                },
                {
                "purpose":"Labor Overload Form Submitted Notification For Labor Office",
                "subject":"Labor Overload Form Submitted Notification",
                "body":'''
                        <p>Dear <strong>Labor Administrator</strong>,</p>
                        <p>&nbsp;</p>
                        <p>There has been an overload form request submitted by <strong>@@Student@@</strong> that needs your attention</p>
                        <p>Please follow this link to check all pending labor overload forms: <a href="@@link@@">@@link@@</a></p>
                            ''',
                "audience":"Labor Office"
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
