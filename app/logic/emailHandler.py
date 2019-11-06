from flask import Flask, request, render_template
from flask_mail import Mail, Message
from app.config.loadConfig import*
from app.models.emailTemplate import*
from app.models.laborReleaseForm import*
from app.models.laborStatusForm import*
from app.models.overloadForm import*
from app.models.formHistory import*
from datetime import datetime
# import app.config
import string
from app import app
import os

class emailHandler():
    def __init__(self, laborStatusKey, formHistoryKey):
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

        self.formHistory = FormHistory.get(FormHistory.formHistoryID == formHistoryKey)
        self.laborStatusForm = LaborStatusForm.get(LaborStatusForm.laborStatusFormID == laborStatusKey)
        self.studentName = self.laborStatusForm.studentSupervisee.FIRST_NAME + " " + self.laborStatusForm.studentSupervisee.LAST_NAME
        self.studentEmail = self.laborStatusForm.studentSupervisee.STU_EMAIL
        self.creatorName = self.formHistory.createdBy.FIRST_NAME + " " + self.formHistory.createdBy.LAST_NAME
        self.creatorEmail = self.formHistory.createdBy.EMAIL
        self.supervisorName = self.laborStatusForm.supervisor.FIRST_NAME + " " + self.laborStatusForm.supervisor.LAST_NAME
        self.supervisorEmail = self.laborStatusForm.supervisor.EMAIL

    def laborReleaseFormEmail(self):
        '''
        Send email to student and supervisor when a release form is created
        '''
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.emailTemplateID == 1)
        releaseFormTemplate = releaseEmailTemplateID.body
        releaseFormTemplate = releaseFormTemplate.replace("@@Student@@", self.studentName)
        releaseFormTemplate = releaseFormTemplate.replace("@@Creator@@", self.creatorName)
        releaseFormTemplate = releaseFormTemplate.replace("@@Position@@", self.laborStatusForm.POSN_CODE+ ", " + self.laborStatusForm.POSN_TITLE)
        releaseFormTemplate = releaseFormTemplate.replace("@@Department@@", self.laborStatusForm.department.DEPT_NAME)



        if self.laborStatusForm.weeklyHours != None:
            weeklyHours = str(self.laborStatusForm.weeklyHours)
            releaseFormTemplate = releaseFormTemplate.replace("@@Hours@@", weeklyHours)
        else:
            contractHours = str(self.laborStatusForm.contractHours)
            releaseFormTemplate = releaseFormTemplate.replace("@@Hours@@", contractHours)

        # date = str(self.laborStatusForm.startDate)
        # releaseFormTemplate = releaseFormTemplate.replace("@@Date@@", date)

        studentMessage = Message(releaseEmailTemplateID.subject, # This is the subject of the E-mail
            recipients=[self.studentEmail])
        studentMessage.html = releaseFormTemplate
        self.mail.send(studentMessage)


    def laborSratusFormEmail(self):
        studentMessage = Message("Labor Realease Form", # This is the subject of the E-mail
            recipients=[self.studentEmail])
        statusEmailTemplateID = EmailTemplate.get(EmailTemplate.emailTemplateID == 1)
        statusFormTemplate = statusEmailTemplateID.body
        statusFormTemplate = string.replace("@@Student@@", self.studentName)
        self.mail.send(statusFormTemplate)

    def LaborOverLoadFormEmail(self):
        studentMessage = Message("Labor Realease Form", # This is the subject of the E-mail
            recipients=[self.studentEmail])
        overloadEmailTemplateID = EmailTemplate.get(EmailTemplate.emailTemplateID == 1)
        overloadFormTemplate = statusEmailTemplateID.body
        overloadFormTemplate = string.replace("@@Student@@", self.studentName)
        self.mail.send(statusFormTemplate)
