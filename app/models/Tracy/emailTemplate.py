#TRACY File
#Modeled after User.py in Advancement Office with inspo from URCPP models
from app.models import *

#Any foreign keys or other imports


#Note: if you update the model, you will need to update the queries to pull the right attributes you want
class EmailTemplate (baseModel):
    emailTemplateID                 = IntegerField(primary_key = True)
    purpose                         = CharField()
    subject                         = CharField()
    body                            = CharField()
    audience                        = CharField()



#Queries as helper functions to user class
####FIX ME: these are currently written as if they were in a class. FIx them to work with the emailTemplate class

    def insert_emailTemplate(self, emailTemplateID, purpose, subject, body):
        try:
            emailTemplate = self.EmailTemplate(emailTemplateID = emailTemplateID, purpose = purpose, subject = subject,
                                body  = body)
            emailTemplate.save()
            return True
        except Exception as e:
            print("EmailTemplate", e)
            return False
