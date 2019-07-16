from app.models import *


class EmailTemplate (baseModel):
    emailTemplateID                 = IntegerField(primary_key=True)
    purpose                         = CharField()
    subject                         = CharField()
    body                            = CharField()
    audience                        = CharField()
