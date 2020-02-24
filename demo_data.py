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
# Positions (TRACY)
#############################
from app.models.Tracy.stuposn import STUPOSN

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
STUPOSN.insert_many(positions).on_conflict_replace().execute()

print("positions (TRACY) added")

#############################
# TRACY Staff
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
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            },

            {
            "PIDM":2,
            "ID": "B12365892",
            "FIRST_NAME":"Jan",
            "LAST_NAME" : "Pearce",
            "EMAIL"  :"pearcej@berea.edu",
            "CPO":"6301",
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            },

            {
            "PIDM":3,
            "ID": "B1236236",
            "FIRST_NAME":"Mario",
            "LAST_NAME" : "Nakazawa",
            "EMAIL"  :"nakazawam@berea.edu",
            "CPO":"6302",
            "ORG":"2150",
            "DEPT_NAME": "Mathematics"
            },

            {
            "PIDM":4,
            "ID": "B1236237",
            "FIRST_NAME":"Megan",
            "LAST_NAME" : "Hoffman",
            "EMAIL"  :"hoffmanm@berea.edu",
            "CPO":"6303",
            "ORG":"2107",
            "DEPT_NAME": "Biology"
            },
            {
            "PIDM":5,
            "ID": "B12365893",
            "FIRST_NAME":"Jasmine",
            "LAST_NAME" : "Jones",
            "EMAIL"  :"jonesj@berea.edu",
            "CPO":"6301",
            "ORG":"2114",
            "DEPT_NAME": "Computer Science"
            }
        ]
stustaff = STUSTAFF.insert_many(staffs).on_conflict_replace().execute()
print(stustaff)
print("staff added")

def insert_to_users(staffs):
    from app.models.user import User
    for sta in staffs[0:2]: #insert staff members into stustaff; Currently just Scott (admin) and Jan (fac/staff)
        try:
            u = User()
            u.PIDM = sta.PIDM
            u.FIRST_NAME = sta.FIRST_NAME
            u.LAST_NAME = sta.LAST_NAME
            u.username = sta.EMAIL.split("@")[0]
            u.EMAIL = sta.EMAIL
            u.CPO = sta.CPO
            u.ORG = sta.ORG
            u.DEPT_NAME = sta.DEPT_NAME
            if u.PIDM == 1:
                u.isLaborAdmin = 1
            u.save()
        except Exception as e:
            print("Failed to insert ", u.username, ": ", e)
insert_to_users(STUSTAFF.select())


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
                },
                # Break Labor Status Forms
                {
                "purpose":"Break Labor Status Form Submitted For Student",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Student@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is very important. Please take a moment to read carefully and review the information. A Labor Status Form has been submitted for you by <strong>@@Creator@@</strong>. Below is the position information for which you have been hired. If you do not accept the terms of this form, you will have 24 hours to contact the supervisor or the Labor Program Office. If we do not hear from you within 24 hours of this notification, it will be determined that it is accepted and the forms will be processed as submitted.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted
                            to await approval. Once this position has been approved, your job will be active to allow for time entry in 24 hours. I
                            f at that time, you cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> You are already working as (Their other Position????) for (their number of hours perweek???).
                            Please note that you are only allowed to work for a maximum of 40 hours per week.</p>
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

                "audience":"student"
                },
                {
                "purpose":"Break Labor Status Form Submitted For Supervisor",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is confirmation that the Labor Program Office has received a Labor Status Form
                            <strong>@@Creator@@</strong> for <strong>Student</strong>. Please take a moment to read carefully and review the information Below is the position information for the student you have requested to hire.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> <strong>@@Student@@</strong>.
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
                "audience":"supervisor"
                },
                {"purpose":"Break Labor Status Form Submitted For Second Supervisor",
                "subject":"Labor Status Form Received",
                "body":'''<p>Dear <strong>@@Supervisor@@</strong>,</p>
                            <p>&nbsp;</p>
                            <p>This email is confirmation that the Labor Program Office has received a Labor Status Form
                            <strong>@@Creator@@</strong> for <strong>Student</strong>. Please take a moment to read carefully and review the information Below is the position information for the student you have requested to hire.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> This does not mean your position is active to begin work, only a status form has been submitted to await approval. Once this position has been approved, the student’s job will be active to allow for time entry in 24 hours. If at that time, the student cannot clock in, please contact the Labor Program Office immediately.</p>
                            <p>&nbsp;</p>
                            <p><strong>NOTICE:</strong> <strong>@@Student@@</strong> is already working with <strong>@@PrimarySupervisor@@</strong>.</p>
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
                "audience":"breakPrimary"
                }
            ]
EmailTemplate.insert_many(emailtemps).on_conflict_replace().execute()
print("emailtemplates added")

print("Dummy data added")
