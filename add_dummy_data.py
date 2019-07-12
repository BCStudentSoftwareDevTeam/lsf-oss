'''Add new fields to this file and run it to add new enteries into your local database.
Chech phpmyadmin to see if your changes are reflected '''
#############################
# USERS
#############################
from app.models.user import User

users = [
     {
         "username": "heggens",
         "firstname": "Scott",
         "lastname": "Heggen"
     },
     {
        "username": "pearcej",
        "firstname": "Jan",
        "lastname": "Pearce"
     }
    ]

User.insert_many(users).on_conflict_replace().execute()


#############################
# Labor Status Forms
#############################
from app.models.laborStatusForm import LaborStatusForm

lsfs = [{
    "laborStatusFormID": 1,
    "term": "Fall 2019",
    "studentSupervisee": "Kat Adams",  #FIXME foreign key eventually
    "primarySupervisor": "Scott Heggen",
    "department": "CS",
    "departmentCode": 2014,
    "jobType": "Primary",
    "position": "S12345",
    "RegularTermHours": 12,
    "startDate": "1/2/3",
    "endDate": "3/2/1",
    "creator": "heggens",
    "createdDate": "1/2/3",
    "formStatus": "Pending"
    },
    {
    "laborStatusFormID": 2,
    "term": "Fall 2019",
    "studentSupervisee": "May Jue",  #FIXME foreign key eventually
    "primarySupervisor": "Bria Williams",
    "department": "CS",
    "departmentCode": 2014,
    "jobType": "Primary",
    "position": "S12345",
    "RegularTermHours": 12,
    "startDate": "1/2/3",
    "endDate": "3/2/1",
    "creator": "heggens",
    "createdDate": "1/2/3",
    "formStatus": "Pending"
    }
]

LaborStatusForm.insert_many(lsfs).on_conflict_replace().execute()


#############################
# Terms
#############################
from app.models.term import Term

terms = [
    {
    "termCode":201612,
    "termName" :"201612's name",
    "termStart":"2017-01-10", #YYYY-MM-DD format.#FIXME: I know this isnt right but idk what the term code above reflects. (ay, spring, etc)
    "termEnd":"2017-05-10",
    "termState":"open",
    },
    {
    "termCode":201712,
    "termName" :"201712's name",
    "termStart":"2018-01-10", #YYYY-MM-DD format.#FIXME: I know this isnt right but idk what the term code above reflects. (ay, spring, etc)
    "termEnd":"2018-05-10",
    "termState":"closed",
    },
    # {
    #     "termID": 2,
    #     "termName": "Fall 2019",
    #     "termCode": 201911,
    #     "active": True
    # },
    # {
    #     "termID": 3,
    #     "termName": "Spring 2018",
    #     "termCode": 201712,
    #     "active": False
    # }
]

Term.insert_many(terms).on_conflict_replace().execute()


#TODO To be continued...
