#Modeled after User.py in Advancement Office with inspo from URCPP models
from app.models.util import *
#Any foreign keys or other imports


#Note: if you update the model, you will need to update the queries to pull the right attributes you want
class emailTemplate (baseModel):
    emailTemplateID                 = PrimaryKeyField()
    purpose                         = CharField()
    subject                         = CharField()
    body                            = Charfield()



#Queries as helper functions to user class
####FIX ME: these are currently written as if they were in a class. FIx them to work with the emailTemplate class

def insert_emailTemplate(self, emailTemplateID, purpose, subject, body):
    try:
        emailTemplate = emailTemplate(emailTemplateID = emailTemplateID, purpose = purpose, subject = subject,
                            body  = body)
        emailTemplate.save()
        return student
    except Exception as e:
        print ("emailTemplate",e)
        return e
