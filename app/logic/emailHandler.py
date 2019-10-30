from flask import Flask, request, render_template
from flask_mail import Mail, Message
from app.config.loadConfig import*
from app.models.emailTemplate import*
# import app.config
import string
from app import app
import os

class emailHandler():
    def __init__(self):
        pass
    def laborReleaseFormEmail(self, recipient):
        print("emails")

        secret_conf = get_secret_cfg()

        app.config.update(
            MAIL_SERVER=secret_conf['MAIL_SERVER'],
            MAIL_PORT=secret_conf['MAIL_PORT'],
            MAIL_USERNAME= secret_conf['MAIL_USERNAME'],
            MAIL_PASSWORD= secret_conf['MAIL_PASSWORD'],
            MAIL_USE_TLS=secret_conf['MAIL_USE_TLS'],
            MAIL_USE_SSL=secret_conf['MAIL_USE_SSL'],
            MAIL_DEFAULT_SENDER=secret_conf['MAIL_DEFAULT_SENDER']

        )

        mail = Mail(app)
        msg = Message("hi", # This is the subject of the E-mail
            recipients=[recipient]) #FIXME: Add email of receiver
        message_to_send = render_template("admin/emailTemplates.html")
        # message_to_send = render_template( 'admin/emailTemplates.html')

        emailTemplateID = EmailTemplate.select()
        for i in emailTemplateID:

            print(i)
        purpose = EmailTemplate.select()
        subject = EmailTemplate.select()
        body = EmailTemplate.select()
        msg.html= render_template( 'admin/emailTemplates.html',
    				            title=('Email Templates'),
                                emailTemplateID = emailTemplateID,
                                purpose = purpose,
                                subject = subject,
                                body = body
                              )
        mail.send(msg)
        print("sent")
    def simpleMethod(self):
        print("hello Augazul")
