'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''
####Add tables that are referenced via foreign key first

from datetime import *
from app.models.Tracy.studata import STUDATA
from app.models.student import Student
from app.models.supervisor import Supervisor
from app.models.Tracy.stuposn import STUPOSN
from app.models.Tracy.stustaff import STUSTAFF
from app.models.Tracy import db
from app.models.student import Student
from app.models.department import Department
from app.models.user import User
from app.models.status import Status
from app.models.historyType import HistoryType
from app.models.term import Term
from app.models.emailTemplate import EmailTemplate
from app.models.laborStatusForm import LaborStatusForm
from app.models.formHistory import FormHistory
from app.models.adminNotes import AdminNotes

#############################
# Students (TRACY)
#############################
studentsTracy = [
                {
                "ID":"B00730361",
                "PIDM":"1",
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
                "PIDM":"2",
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
                "PIDM":"3",
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
                "ID":"B00785329",
                "PIDM":"4",
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
students = []
for student in studentsTracy:
    # Add to Tracy db
    db.session.add(STUDATA(**student))
    db.session.commit()

    # Set up lsf db data
    del student["PIDM"]
    students.append(student)
Student.insert_many(students).on_conflict_replace().execute()
print(" * students (TRACY) added")

#############################
# Positions (TRACY)
#############################
positions = [
            {
            "POSN_CODE": "S61407",
            "POSN_TITLE": "Student Programmer",
            "WLS": "1",
            "ORG" : "2114",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61408",
            "POSN_TITLE": "Research Associate",
            "WLS": "5",
            "ORG" : "2114",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61419",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "3",
            "ORG" : "2114",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61420",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "5",
            "ORG" : "2147",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Technology and Applied Design"
            },
            {
            "POSN_CODE": "S61421",
            "POSN_TITLE": "TA",
            "WLS": "6",
            "ORG" : "2114",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Computer Science"
            },
            {
            "POSN_CODE": "S61427",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "2",
            "ORG" : "2150",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Mathematics"
            },
            {
            "POSN_CODE": "S61430",
            "POSN_TITLE": "Teaching Associate",
            "WLS": "5",
            "ORG" : "2107",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Biology"
            },
            {
            "POSN_CODE": "S61443",
            "POSN_TITLE": "Lab Assistant",
            "WLS": "6",
            "ORG" : "2107",
            "ACCOUNT":"6740",
            "DEPT_NAME":"Biology"
            }
]
# Add to Tracy db
for position in positions:
    db.session.add(STUPOSN(**position))
    db.session.commit()

print(" * positions (TRACY) added")

#############################
# TRACY Staff
#############################
staffs = [

            {
            "ID": "B12361006",
            "PIDM":1,
            "FIRST_NAME":"Scott",
            "LAST_NAME" : "Heggen",
            "EMAIL"  :"heggens@berea.edu",
            "CPO":"6300",
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            },

            {
            "ID": "B12365892",
            "PIDM":2,
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            },

            {
            "ID": "B1236236",
            "PIDM":3,
            "FIRST_NAME":"Mario",
            "LAST_NAME" : "Nakazawa",
            "EMAIL"  :"nakazawam@berea.edu",
            "CPO":"6302",
            "ORG":"2150",
            "DEPT_NAME": "Mathematics"
            },

            {
            "ID": "B1236237",
            "PIDM":4,
            "FIRST_NAME":"Megan",
            "LAST_NAME" : "Hoffman",
            "EMAIL"  :"hoffmanm@berea.edu",
            "CPO":"6303",
            "ORG":"2107",
            "DEPT_NAME": "Biology"
            },
            {
            "ID": "B12365893",
            "PIDM":5,
            "FIRST_NAME":"Jasmine",
            "LAST_NAME" : "Jones",
            "EMAIL"  :"jonesj@berea.edu",
            "CPO":"6301",
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            },
            {
            "ID": "B00005893",
            "PIDM":6,
            "FIRST_NAME":"Brian",
            "LAST_NAME" : "Ramsay",
            "EMAIL"  :"ramsayb2@berea.edu",
            "CPO":"6305",
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            },
            {
            "ID": "B00841417",
            "PIDM":7,
            "FIRST_NAME":"Alex",
            "LAST_NAME" : "Bryant",
            "EMAIL"  :"bryantal@berea.edu",
            "CPO":"420",
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            }
        ]
for staff in staffs:
    # Add to Tracy db
    db.session.add(STUSTAFF(**staff))
    db.session.commit()

    # Add to users
    try:
        u = User()
        u.PIDM = staff['PIDM']
        u.FIRST_NAME = staff['FIRST_NAME']
        u.LAST_NAME = staff['LAST_NAME']
        u.username = staff['EMAIL'].split("@")[0]
        u.EMAIL = staff['EMAIL']
        u.CPO = staff['CPO']
        u.ID = staff['ID']
        u.ORG = staff['ORG']
        u.DEPT_NAME = staff['DEPT_NAME']
        if u.PIDM == 1:
            u.isLaborAdmin = 1
        u.save()
    except Exception as e:
        print(" * Failed to insert ", u.username, ": ", e)

print(" * staff added")

Supervisor.insert_many(staffs).on_conflict_replace().execute()
print(" * staff added")
# insert_to_users(STUSTAFF.select())


#############################
# Users
#############################
users = [
        {
        "Student": None,
        "Supervisor": "B12361006",
        "username": "heggens",
        "isLaborAdmin": 1,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": None,
        "Supervisor": "B12365892",
        "username": "pearcej",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": None,
        "Supervisor": "B1236236",
        "username": "nakazawam",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": None,
        "Supervisor": "B1236237",
        "username": "hoffmanm",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": None,
        "Supervisor": "B12365893",
        "username": "jonesj",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": None,
        "Supervisor": "B00005893",
        "username": "ramsayb2",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": "B00730361",
        "Supervisor": None,
        "username": "jamalie",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": "B00734292",
        "Supervisor": None,
        "username": "cruzg",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": "B00785329",
        "Supervisor": None,
        "username": "adamskg",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        },
        {
        "Student": "B00841417",
        "Supervisor": "B00841417",
        "username": "bryantal",
        "isLaborAdmin": None,
        "isFinancialAidAdmin": None,
        "isSaasAdmin": None
        }
        ]
User.insert_many(users).on_conflict_replace().execute()
print(" * users added")



#############################
# Department
#############################
departments = [
            {
              "departmentID":1,
              "DEPT_NAME": "Computer Science",
              "ACCOUNT": "6740",
              "ORG": "2114",
              "departmentCompliance": 1
            },
            {
              "departmentID":2,
              "DEPT_NAME": "Technology and Applied Design",
              "ACCOUNT": "6740",
              "ORG": "2147",
              "departmentCompliance": 1
            },
            {
              "departmentID":3,
              "DEPT_NAME": "Mathematics",
              "ACCOUNT": "6740",
              "ORG": "2150",
              "departmentCompliance": 1
            },
            {
              "departmentID":4,
              "DEPT_NAME": "Biology",
              "ACCOUNT": "6740",
              "ORG": "2107",
              "departmentCompliance": 1
            },
        ]
Department.insert_many(departments).on_conflict_replace().execute()
print(" * departments added")

#############################
# Status
#############################
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
print(" * status added")

#############################
# History Type
#############################
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
print(" * history types added")

#############################
# Term
#############################
terms = [
            {
            "termCode":"202000",
            "termName": "AY 2020-2021",
            "termStart":"2020-08-01",
            "termEnd" : "2021-05-01",
            "termState": 1,
            "primaryCutOff": "2020-09-01",
            "adjustmentCutOff": "2020-09-01"
            },
            {
            "termCode":"202001",
            "termName": "Thanksgiving Break 2020",
            "termStart":"2020-08-01",
            "termEnd" : "2021-05-01",
            "termState": 0,
            "primaryCutOff": "2020-09-01",
            "adjustmentCutOff": "2020-09-01",
            "isBreak": 1
            }
       ]
Term.insert_many(terms).on_conflict_replace().execute()
print(" * terms added")

#############################
# Create a Pending Labor Status Form
#############################
LaborStatusForm.insert([{
            "laborStatusFormID": 2,
            "termCode_id": "202000",
            "studentName": "Alex Bryant",
            "studentSupervisee_id": "B00841417",
            "supervisor_id": "B12361006",
            "department_id": 1,
            "jobType": "Primary",
            "WLS": 1,
            "POSN_TITLE": "Student Programmer",
            "POSN_CODE": "S61407",
            "weeklyHours": 10,
            "startDate": "2020-04-01",
            "endDate": "2020-09-01"
        }]).on_conflict_replace().execute()
FormHistory.insert([{
            "formHistoryID": 2,
            "formID_id": "2",
            "historyType_id": "Labor Status Form",
            "createdBy_id": 1,
            "createdDate": "2020-04-14",
            "status_id": "Pending"
        }]).on_conflict_replace().execute()


#############################
#emailtemplates
#############################
emailtemps= [
                {
                "purpose":"Labor Status Form Submitted For Student",
                "formType":"Labor Status Form",
                "action":"Submitted",
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

                "audience":"Student"
                 },
                {
                "purpose":"Secondary Position Labor Status Form Submitted",
                "formType":"Secondary Labor Status Form",
                "action":"Submitted",
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
                "audience":"Supervisor"
                },
                {
                "purpose":"Primary Position Labor Status Form Submitted",
                "formType":"Labor Status Form",
                "action":"Submitted",
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
                "audience":"Supervisor"
                },
                #LSF approved
                {
                "purpose":"Labor Status Form Approved For Student",
                "formType":"Labor Status Form",
                "action":"Approved",
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
                "audience":"Student"
                },
                {
                "purpose":"Primary Position Labor Status Form Approved",
                "formType":"Labor Status Form",
                "action":"Approved",
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
                "audience":"Supervisor"
                },

                {
                "purpose":"Secondary Position Labor Status Form Approved",
                "formType":"Secondary Labor Status Form",
                "action":"Approved",
                "subject":"Labor Status Form Approved",
                "body":'''

                            ''',
                "audience":"Supervisor"
                },
                #LSF Rejected
                {
                "purpose":"Labor Status Form Rejected For Student",
                "formType":"Labor Status Form",
                "action":"Rejected",
                "subject":"Labor Status Form Rejected",
                "body":'''
                            ''',
                "audience":"Student"
                },
                {
                "purpose":"Secondary Position Labor Status Form Rejected",
                "formType":"Secondary Labor Status Form",
                "action":"Rejected",
                "subject":"Labor Status Form Rejected",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong> and <strong>@@Primsupr@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>A Labor Status Form previously submitted by you for
                            <strong>@@Student@@</strong>, <strong>@@StudB@@</strong> hiring him/her to work in a secondary position has been Denied. This is an informational email to you as the supervisor for the primary labor position.</p>
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
                "audience":"Supervisor"
                },
                {
                "purpose":"Primary Position Labor Status Form Rejected",
                "formType":"Labor Status Form",
                "action":"Rejected",
                "subject":"Labor Status Form Rejected",
                "body":'''
                            ''',
                "audience":"Supervisor"
                },
                #LSF modified
                {
                "purpose":"Labor Status Form Modified For Student",
                "formType":"Labor Status Form",
                "action":"Modified",
                "subject":"Labor Status Form Modified",
                "body":'''
                            ''',
                "audience":"Student"
                },
                {
                "purpose":"Labor Status Form Modified For Supervisor",
                "formType":"Labor Status Form",
                "action":"Modified",
                "subject":"Labor Status Form Modified",
                "body":'''
                            ''',
                "audience":"Supervisor"
                },
                #LRF Submitted
                {
                "purpose":"Labor Release Form Submitted For Student",
                "formType":"Labor Release Form",
                "action":"Submitted",
                "subject":"Labor Release Form Submitted",
                "body":'''
                            ''',
                "audience":"Student"
                },
                {
                "purpose":"Labor Release Form Submitted For Supervisor",
                "formType":"Labor Release Form",
                "action":"Submitted",
                "subject":"Labor Release Form Submitted",
                "body":'''
                            ''',
                "audience":"Supervisor"
                },
                #LRF approved

                {
                "purpose":"Labor Release Form Approved For Student",
                "formType":"Labor Release Form",
                "action":"Approved",
                "subject":"Labor Release Form Approved",
                "body":'''<p>Dear <strong>@@Student@@</strong>,</p>
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
                "audience":"Student"
                },
                {
                "purpose":"Labor Release Form Approved For Supervisor",
                "formType":"Labor Release Form",
                "action":"Approved",
                "subject":"Labor Release Form Approved",
                "body":'''
                            ''',
                "audience":"Supervisor"
                },
                #LRF Rejected
                {
                "purpose":"Labor Release Form Rejected For Student",
                "formType":"Labor Release Form",
                "action":"Rejected",
                "subject":"Labor Release Form Rejected",
                "body":'''
                            ''',
                "audience":"Student"
                },
                {
                "purpose":"Labor Release Form Rejected For Supervisor",
                "formType":"Labor Release Form",
                "action":"Rejected",
                "subject":"Labor Release Form Rejected",
                "body":'''
                            ''',
                "audience":"Supervisor"
                },
                #LOF
                {
                "purpose":"Labor Overload Form Submitted For Student",
                "formType":"Labor Overload Form",
                "action":"Submitted",
                "subject":"Labor Overload Form Submitted",
                "body":'''
                    <p>Dear <strong>@@Student@@</strong>,</p>
                    <p>&nbsp;</p>
                    <p>Please follow the attached link to verify information needed for the approval of an overload form: <a href="@@link@@">@@link@@</a></p>
                    ''',
                "audience":"Student"
                },
                {
                "purpose":"Labor Overload Form Submitted For Supervisor",
                "formType":"Labor Overload Form",
                "action":"Submitted",
                "subject":"Labor Overload Form Submitted",
                "body":'''
                            ''',
                "audience":"Supervisor"
                },
                {
                "purpose":"Labor Overload Form Approved For Student",
                "formType":"Labor Overload Form",
                "action":"Approved",
                "subject":"Labor Overload Form Approved",
                "body":'''
                            ''',
                "audience":"Student"
                },
                {
                "purpose":"Labor Overload Form Approved For Supervisor",
                "formType":"Labor Overload Form",
                "action":"Approved",
                "subject":"Labor Overload Form Approved",
                "body":'''
                            ''',
                "audience":"Supervisor"
                },
                {
                "purpose":"Labor Overload Form Rejected For Student",
                "formType":"Labor Overload Form",
                "action":"Rejected",
                "subject":"Labor Overload Form Rejected",
                "body":'''
                            ''',
                "audience":"Student"
                },
                #SAAS
                {
                "purpose":"SAAS and Financial Aid Office",
                "formType":"Labor Overload Form",
                "action":"Submitted",
                "subject":"Overload Verification",
                "body":'''
                    <p>Please follow the attached link to verify information needed for the approval of an overload form: <a href="@@link@@">@@link@@</a></p>
                            ''',
                "audience":"SAAS and Financial Aid Office"
                },
                # Break Labor Status Forms
                {
                "purpose":"Break Labor Status Form Submitted For Student",
                "formType":"Break Labor Status Form",
                "action":"Submitted",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Student@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is very important. Please take a moment to read carefully and review the information. A Labor Status Form has been submitted for you by <strong>@@Creator@@</strong>. Below is the position information for which you have been hired. If you do not accept the terms of this form, you will have 24 hours to contact the supervisor or the Labor Program Office. If we do not hear from you within 24 hours of this notification, it will be determined that it is accepted and the forms will be processed as submitted.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, your job will be active to allow for time entry in 24 hours. If at that time, you cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> There is already another labor position submitted for you. (put position and x hrs/week???)
                             Please be aware that you are only allowed to work maximum of 40 hours per week if you are not taking any classes.</p>
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
                "audience":"Student"
                },
                {
                "purpose":"Break Labor Status Form Submitted For Supervisor", #Original name: Break Labor Status Form Submitted For Supervisor
                "formType":"Break Labor Status Form",
                "action":"Submitted",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is confirmation that the Labor Program Office has received a Labor Status Form for Break by
                            <strong>@@Creator@@</strong> for <strong>@@Student@@</strong>. Please take a moment to read carefully and review the information Below is the position information for the student you have requested to hire.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            Please note that students are only allowed to work for a maximum of 40 hours per week.</p>
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
                "audience":"Supervisor"
                },
                {
                "purpose":"Break Labor Status Form Submitted For Supervisor on Second LSF", #Original name: Break Labor Status Form Submitted For Supervisor on Second LSF
                "formType":"Second Break Labor Status Form",
                "action":"Submitted",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is confirmation that the Labor Program Office has received a Labor Status Form for Break position by
                            <strong>@@Creator@@</strong> for <strong>@@Student@@</strong>. Please take a moment to read carefully and review the information Below is the position information for the student you have requested to hire.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> <strong>@@Student@@</strong> is already working with <strong>@@PrimarySupervisor@@</strong>.
                            Please note that students are only allowed to work for a maximum of 40 hours per week.</p>
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
                "audience":"Supervisor"
                },
                {"purpose":"Break Labor Status Form Submitted For Second Supervisor", # Original name: Break Labor Status Form Submitted For Second Supervisor
                "formType":"Second Break Labor Status Form",
                "action":"Submitted",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@PrimarySupervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is notify you that @@Supervisor@@ (@@SupervisorEmail@@) has submitted another labor status form for @@Student@@</p>
                            <p>&nbsp;</p>
                            Please note that students are only allowed to work for a maximum of 40 hours per week.</p>
                            <p>&nbsp;</p>
                            <p>If you have any further questions or concerns, contact the Labor Program Office at ext. 3611.</p>
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
                "audience":"Break Supervisor"
                },
                {"purpose":"Labor Overload Form Submitted Notification For Student",
                "formType":"Labor Overload Form",
                "action":"Notification",
                "subject":"Labor Overload Form Student Reason",
                "body":'',
                "audience":"Student"
                },
                {"purpose":"Labor Overload Form Submitted Notification For Labor Office",
                "formType":"Labor Overload Form",
                "action":"Notification",
                "subject":"Labor Overload Form Student Reason",
                "body":'',
                "audience":"Labor Office"
                }
            ]
EmailTemplate.insert_many(emailtemps).on_conflict_replace().execute()
print(" * emailtemplates added")

#############################
#emailtemplates
#############################
adminNotes = [
            {
            "noteHistoryID": 1,
            "formID_id": 2,
            "date":"2020-01-01",
            "createdBy" : 1,
            "notesContents": "This is the first note"
            },
            {
            "noteHistoryID": 2,
            "formID_id": 2,
            "date":"2020-02-01",
            "createdBy" : 1,
            "notesContents": "This is the second note"
            },
       ]
AdminNotes.insert_many(adminNotes).on_conflict_replace().execute()
print(" * laborOfficeNotes added")

print("Dummy data added")
