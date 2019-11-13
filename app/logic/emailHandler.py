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
        self.studentEmail = self.laborStatusForm.studentSupervisee.STU_EMAIL
        self.creatorEmail = self.formHistory.createdBy.EMAIL
        self.supervisorEmail = self.laborStatusForm.supervisor.EMAIL
        self.date = self.laborStatusForm.startDate.strftime("%m/%d/%Y")
        self.weeklyHours = str(self.laborStatusForm.weeklyHours)
        self.contractHours = str(self.laborStatusForm.contractHours)

        self.primaryForm = LaborStatusForm.get(LaborStatusForm.jobType == "Primary" and LaborStatusForm.studentSupervisee == self.laborStatusForm.studentSupervisee and LaborStatusForm.termCode == self.laborStatusForm.termCode)
        self.primaryEmail = self.primaryForm.supervisor.EMAIL
        self.releaseReason = ""
        self.date = ""
    def laborReleaseFormEmail(self):
        self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
        self.releaseReason = self.formHistory.releaseForm.reasonForRelease
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Approval of Labor Release Form to Student")
        releaseFormTemplate = releaseEmailTemplateID.body
        releaseFormTemplate = self.replaceText(releaseFormTemplate)

        studentMessage = Message(releaseEmailTemplateID.subject, # This is the subject of the E-mail
            recipients=[self.studentEmail])
        studentMessage.html = releaseFormTemplate
        self.mail.send(studentMessage)


    def laborStatusFormSubmitted(self):
        """
        This method is for sending email to the student when a Labor Status Form has been created. The email template's keywords are replace with the LSF informations.
        """
        StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Submission of Status Form to Student")
        StatusFormTemplate = StatusFormEmailTemplateID.body
        StatusFormTemplate = self.replaceText(StatusFormTemplate)

        studentMessage = Message(StatusFormEmailTemplateID.subject, # This is the subject of the E-mail
            recipients=[self.studentEmail])
        studentMessage.html = StatusFormTemplate
        self.mail.send(studentMessage)

        if self.laborStatusForm.jobType == "Secondary":
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Supervisors, Form Received (Secondary)")
            StatusFormTemplate = SupervisorEmailTemplateID.body
            StatusFormTemplate = self.replaceText(StatusFormTemplate)
            supervisorMessage = Message(SupervisorEmailTemplateID.subject, # This is the subject of the E-mail
                recipients=[self.supervisorEmail, self.primaryEmail])
            supervisorMessage.html = StatusFormTemplate
            self.mail.send(supervisorMessage)
        else:
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Supervisor, Form Received")
            StatusFormTemplate = SupervisorEmailTemplateID.body
            StatusFormTemplate = self.replaceText(StatusFormTemplate)
            supervisorMessage = Message(SupervisorEmailTemplateID.subject, # This is the subject of the E-mail
                recipients=[self.supervisorEmail])
            supervisorMessage.html = StatusFormTemplate
            self.mail.send(supervisorMessage)

    def laborStatusFormApprove(self):
        """
        """
        #Email for Student
        StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Student")
        approveFormTemplate = StatusFormEmailTemplateID.body
        approveFormTemplate = self.replaceText(approveFormTemplate)

        studentMessage = Message(StatusFormEmailTemplateID.subject, # This is the subject of the E-mail
            recipients=[self.studentEmail])
        studentMessage.html = approveFormTemplate
        self.mail.send(studentMessage)

        # if self.laborStatusForm.jobType == "Secondary":
        #     SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Supervisors, Form Received (Secondary)")
        #     StatusFormTemplate = SupervisorEmailTemplateID.body
        #     StatusFormTemplate = self.replaceText(StatusFormTemplate)
        #     supervisorMessage = Message(SupervisorEmailTemplateID.subject, # This is the subject of the E-mail
        #         recipients=[self.supervisorEmail, self.primaryEmail])
        #     supervisorMessage.html = StatusFormTemplate
        #     self.mail.send(supervisorMessage)
        # else:
        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Supervisor")
        StatusFormTemplate = SupervisorEmailTemplateID.body
        if self.laborStatusForm.jobType == "Secondary":
            StatusFormTemplate = StatusFormTemplate.replace("@@Supervisor@@", self.laborStatusForm.supervisor.FIRST_NAME + " " + self.laborStatusForm.supervisor.LAST_NAME + " and " + self.primaryForm.supervisor.FIRST_NAME + " " + self.primaryForm.supervisor.LAST_NAME)
        StatusFormTemplate = self.replaceText(StatusFormTemplate)
        supervisorMessage = Message(SupervisorEmailTemplateID.subject, # This is the subject of the E-mail
            recipients=[self.supervisorEmail, self.primaryEmail])
        supervisorMessage.html = StatusFormTemplate
        self.mail.send(supervisorMessage)


    def LaborOverLoadFormEmail(self):
        studentMessage = Message("Labor Realease Form", # This is the subject of the E-mail
            recipients=[self.studentEmail])
        overloadEmailTemplateID = EmailTemplate.get(EmailTemplate.emailTemplateID == 1)
        overloadFormTemplate = statusEmailTemplateID.body
        overloadFormTemplate = string.replace("@@Student@@", self.studentName)
        self.mail.send(statusFormTemplate)

    def replaceText(self, form):
        """
        """
        form = form.replace("@@Creator@@", self.formHistory.createdBy.FIRST_NAME + " " + self.formHistory.createdBy.LAST_NAME)
        form = form.replace("@@Supervisor@@", self.laborStatusForm.supervisor.FIRST_NAME + " " + self.laborStatusForm.supervisor.LAST_NAME)
        form = form.replace("@@Primsupr@@", self.primaryForm.supervisor.FIRST_NAME + " " + self.primaryForm.supervisor.LAST_NAME)
        form = form.replace("@@Student@@", self.laborStatusForm.studentSupervisee.FIRST_NAME + " " + self.laborStatusForm.studentSupervisee.LAST_NAME)
        form = form.replace("@@StudB@@", self.laborStatusForm.studentSupervisee.ID)
        form = form.replace("@@Position@@", self.laborStatusForm.POSN_CODE+ ", " + self.laborStatusForm.POSN_TITLE)
        form = form.replace("@@Department@@", self.laborStatusForm.department.DEPT_NAME)
        form = form.replace("@@WLS@@", self.laborStatusForm.WLS)
        if self.laborStatusForm.weeklyHours != None:
            form = form.replace("@@Hours@@", self.weeklyHours)
        else:
            form = form.replace("@@Hours@@", self.contractHours)
        form = form.replace("@@Date@@", self.date)
        form = form.replace("@@ReleaseReason@@", self.releaseReason)
        form = form.replace("@@ReleaseDate@@", self.releaseDate)

        return(form)
