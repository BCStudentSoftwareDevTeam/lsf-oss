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

        self.mail = Mail(app)


    def laborReleaseFormEmail(self, recipient):
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.emailTemplateID == 1)
        string = releaseEmailTemplateID.body
        string = string.replace("Student", "Ela")
        print(string)
        msg = Message(releaseEmailTemplateID.subject, # This is the subject of the E-mail
            recipients=[recipient])
        # message_to_send = render_template("admin/emailTemplates.html")
        # # message_to_send = render_template( 'admin/emailTemplates.html')
        #
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.emailTemplateID == 1)

        purpose = EmailTemplate.select()
        subject = EmailTemplate.select()
        body = EmailTemplate.select()
        # msg.html= render_template( 'admin/sendEmailTemplate.html',
    	# 			            title=('Email Templates'),
        #                         emailTemplateID = releaseEmailTemplateID,
        #                         purpose = purpose,
        #                         subject = subject,
        #                         body = body
        #                       )
        msg.html = string
        # msg.body = releaseEmailTemplateID.body
        #
        # msg.body = render_template(releaseEmailTemplateID.body)
        self.mail.send(msg)
        print("sent")

    def laborSratusFormEmail(self, recipient):
        msg = Message("Labor Realease Form", # This is the subject of the E-mail
            recipients=[recipient])

    def LaborOverLoadFormEmail(self, recipient):
        msg = Message("Labor Realease Form", # This is the subject of the E-mail
            recipients=[recipient])
