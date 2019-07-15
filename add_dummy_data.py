'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected
This file will need to be changed if the format of models changes (new fields, dropping fields, renaming...)'''
#############################
# USERS
#############################
from app.models.user import User

users = [
     # {
     #     "username": "heggens",
     #     "firstName": "Scott",
     #     "lastName": "Heggen",
     #     "email":"heggens@berea.edu",
     #
     # },
     # {
     #    "username": "pearcej",
     #    "firstname": "Jan",
     #    "lastname": "Pearce"
     # },
     ###NEW FORMAT:###
     {
     "username": "heggens",
     "FIRST_NAME":"Scott",
     "LAST_NAME": "Heggen"
     }
    ]

User.insert_many(users).on_conflict_replace().execute()


#############################
# Labor Status Forms
#############################
from app.models.laborStatusForm import LaborStatusForm

lsfs = [
    # {
    # "laborStatusFormID": 1,
    # "term": "Fall 2019",
    # "studentSupervisee": "Kat Adams",  #FIXME foreign key eventually
    # "primarySupervisor": "Scott Heggen",
    # "department": "CS",
    # "departmentCode": 2014,
    # "jobType": "Primary",
    # "position": "S12345",
    # "RegularTermHours": 12,
    # "startDate": "1/2/3",
    # "endDate": "3/2/1",
    # "creator": "heggens",
    # "createdDate": "1/2/3",
    # "formStatus": "Pending"
    # },
    # {
    # "laborStatusFormID": 2,
    # "term": "Fall 2019",
    # "studentSupervisee": "May Jue",  #FIXME foreign key eventually
    # "primarySupervisor": "Bria Williams",
    # "department": "CS",
    # "departmentCode": 2014,
    # "jobType": "Primary",
    # "position": "S12345",
    # "RegularTermHours": 12,
    # "startDate": "1/2/3",
    # "endDate": "3/2/1",
    # "creator": "heggens",
    # "createdDate": "1/2/3",
    # "formStatus": "Pending"
    # },
    #######updated format
    {
    "laborStatusFormID":1,
    "term": "Fall 2019",#FIXME foreign key eventually
    "studentSupervisee": "Kat Adams",  #FIXME foreign key eventually
    "primarySupervisor": "Scott Heggen",#FIXME foreign key eventually
    "department": "CS", #FIXME: Foreign key eventually
    "jobType": "Primary",
    "WLS":"WLS-1", #FIXME: idk how this is gonna be formatted
    "POSN_TITLE" :"Student programmer",
    "POSN_CODE": "S12345",
    "weeklyHours":12,
    "startDate": "1/2/3",
    "endDate": "3/2/1"
    }
]

LaborStatusForm.insert_many(lsfs).on_conflict_replace().execute()


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
    #add more term cases here
]

Term.insert_many(terms).on_conflict_replace().execute()
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

print("Dummy data added")

#TODO To be continued...
