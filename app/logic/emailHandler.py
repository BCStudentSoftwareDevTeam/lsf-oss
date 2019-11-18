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
        self.releaseDate = ""

    def laborStatusFormSubmitted(self):
        """
        This method is for sending email to the student when a Labor Status Form has been created. The email template's keywords are replace with the LSF informations.
        """
        StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Student")
        self.sendEmail(StatusFormEmailTemplateID, "student")

        if self.laborStatusForm.jobType == "Secondary":
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Secondary")
            self.sendEmail(SupervisorEmailTemplateID, "secondary")
        else:
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Primary")
            self.sendEmail(SupervisorEmailTemplateID, "supervisor")

    def laborStatusFormApproved(self):
        #Email for Student
        StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Student")
        self.sendEmail(StatusFormEmailTemplateID, "student")

        #send to supervisor
        if self.laborStatusForm.jobType == "Secondary":
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Secondary")
            self.sendEmail(SupervisorEmailTemplateID, "secondary")
        else:
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Primary")
            self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborStatusFormRejected(self):
        #Email for Student
        StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Rejected For Student")
        self.sendEmail(StatusFormEmailTemplateID, "student")

        #send to supervisor
        if self.laborStatusForm.jobType == "Secondary":
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Rejected For Secondary")
            self.sendEmail(SupervisorEmailTemplateID, "secondary")
        else:
            SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Rejected For Primary")
            self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborStatusFormModified(self):
        StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Modified For Student")
        self.sendEmail(StatusFormEmailTemplateID, "student")

        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Modified For Supervisor")
        self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborReleaseFormSubmitted(self):
        self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
        self.releaseReason = self.formHistory.releaseForm.reasonForRelease
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Submitted For Student")
        self.sendEmail(releaseEmailTemplateID, "student")

        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Submitted For Supervisor")
        self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborReleaseFormApproved(self):
        self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
        self.releaseReason = self.formHistory.releaseForm.reasonForRelease
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Approved For Student")
        self.sendEmail(releaseEmailTemplateID, "student")

        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Approved For Supervisor")
        self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborReleaseFormRejected(self):
        self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
        self.releaseReason = self.formHistory.releaseForm.reasonForRelease
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Rejected For Student")
        self.sendEmail(releaseEmailTemplateID, "student")

        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Rejected For Supervisor")
        self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def LaborOverLoadFormSubmitted(self):
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Submitted For Student")
        self.sendEmail(releaseEmailTemplateID, "student")

        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Submitted For Supervisor")
        self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def LaborOverLoadFormApproved(self):
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Approved For Student")
        self.sendEmail(releaseEmailTemplateID, "student")

        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Approved For Supervisor")
        self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def LaborOverLoadFormRejected(self):
        releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Rejected For Student")
        self.sendEmail(releaseEmailTemplateID, "student")

        SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Rejected For Supervisor")
        self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def SASS(self):
        pass

    def sendEmail(self, template, sendTo):
        formTemplate = template.body
        formTemplate = self.replaceText(formTemplate)

        if sendTo == "student":
            message = Message(template.subject,
                recipients=[self.studentEmail])
        elif sendTo == "secondary":
            message = Message(template.subject,
                recipients=[self.supervisorEmail, self.primaryEmail])
        else:
            message = Message(template.subject,
                recipients=[self.supervisorEmail])
        message.html = formTemplate
        self.mail.send(message)

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
