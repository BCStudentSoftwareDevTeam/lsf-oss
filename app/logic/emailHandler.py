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
    def __init__(self, formHistoryKey):
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
        self.laborStatusForm = self.formHistory.formID
        self.studentEmail = self.laborStatusForm.studentSupervisee.STU_EMAIL
        self.creatorEmail = self.formHistory.createdBy.EMAIL
        self.supervisorEmail = self.laborStatusForm.supervisor.EMAIL
        self.date = self.laborStatusForm.startDate.strftime("%m/%d/%Y")
        self.weeklyHours = str(self.laborStatusForm.weeklyHours)
        self.contractHours = str(self.laborStatusForm.contractHours)

        self.primaryForm = LaborStatusForm.get(LaborStatusForm.jobType == "Primary" and LaborStatusForm.studentSupervisee == self.laborStatusForm.studentSupervisee and LaborStatusForm.termCode == self.laborStatusForm.termCode)
        self.primaryEmail = self.primaryForm.supervisor.EMAIL

        try:
            self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
            self.releaseReason = self.formHistory.releaseForm.reasonForRelease

        except Exception as e:
            # print type(e)
            print (e)
            self.releaseReason = ""
            self.releaseDate = ""
        self.link = ""



    # The methods of this class each handle a different email situation. Some of the methods need to handle
    # "primary" and "secondary" forms differently, but a majority do not need to differentiate between the two.
    # Every method will use the replaceText and sendEmail methods to acomplish the email sending.
    # The email templates are stored inside of the emailHandler model, and depending on which email template
    # is pulled from the model, and replaceText method will replace the neccesary keywords with the correct data.
    # The sendEmail method will handle all of the email sending once the email template has been populated.
    def laborStatusFormSubmitted(self):
        self.template("Labor Status Form Submitted For Student",
                      "Labor Status Form Submitted For Primary",
                      "Labor Status Form Submitted For Secondary")

        # var1 = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Student")
        # var2 = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Primary")
        # var3 = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Secondary")
        # self.template(var1, var2, var3)
        #
        # StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Student")
        # self.sendEmail(StatusFormEmailTemplateID, "student")
        #
        # if self.laborStatusForm.jobType == "Secondary":
        #     SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Secondary")
        #     self.sendEmail(SupervisorEmailTemplateID, "secondary")
        # else:
        #     SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Submitted For Primary")
        #     self.sendEmail(SupervisorEmailTemplateID, "supervisor")

    def template(self, studentEmailPurpose, primaryEmailPurpose, secondaryEmailPurpose = False):
        studentEmail = EmailTemplate.get(EmailTemplate.purpose == studentEmailPurpose)
        self.sendEmail(studentEmail, "student")

        if secondaryEmailPurpose == False:
            primaryEmail = EmailTemplate.get(EmailTemplate.purpose == primaryEmailPurpose)
            self.sendEmail(primaryEmail, "supervisor")
        else:
            if self.laborStatusForm.jobType == "Secondary":
                secondaryEmail = EmailTemplate.get(EmailTemplate.purpose == secondaryEmailPurpose)
                self.sendEmail(secondaryEmail, "secondary")
            else:
                primaryEmail = EmailTemplate.get(EmailTemplate.purpose == primaryEmailPurpose)
                self.sendEmail(primaryEmail, "supervisor")


    def laborStatusFormApproved(self):
        self.template("Labor Status Form Approved For Student",
                      "Labor Status Form Approved For Primary",
                      "Labor Status Form Approved For Secondary")
        # StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Student")
        # self.sendEmail(StatusFormEmailTemplateID, "student")
        #
        # if self.laborStatusForm.jobType == "Secondary":
        #     SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Secondary")
        #     self.sendEmail(SupervisorEmailTemplateID, "secondary")
        # else:
        #     SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Approved For Primary")
        #     self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborStatusFormRejected(self):
        self.template("Labor Status Form Rejected For Student",
                      "Labor Status Form Rejected For Primary",
                      "Labor Status Form Rejected For Secondary")
        # StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Rejected For Student")
        # self.sendEmail(StatusFormEmailTemplateID, "student")
        #
        # if self.laborStatusForm.jobType == "Secondary":
        #     SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Rejected For Secondary")
        #     self.sendEmail(SupervisorEmailTemplateID, "secondary")
        # else:
        #     SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Rejected For Primary")
        #     self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborStatusFormModified(self):
        self.template("Labor Status Form Modified For Student",
                      "Labor Status Form Modified For Supervisor")
        # StatusFormEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Modified For Student")
        # self.sendEmail(StatusFormEmailTemplateID, "student")
        #
        # SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Status Form Modified For Supervisor")
        # self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborReleaseFormSubmitted(self):
        self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
        self.releaseReason = self.formHistory.releaseForm.reasonForRelease
        self.template("Labor Release Form Submitted For Student",
                      "Labor Release Form Submitted For Supervisor")
        # releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Submitted For Student")
        # self.sendEmail(releaseEmailTemplateID, "student")
        #
        # SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Submitted For Supervisor")
        # self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborReleaseFormApproved(self):
        self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
        self.releaseReason = self.formHistory.releaseForm.reasonForRelease
        self.template("Labor Release Form Approved For Student",
                      "Labor Release Form Approved For Supervisor")
        # releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Approved For Student")
        # self.sendEmail(releaseEmailTemplateID, "student")
        #
        # SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Approved For Supervisor")
        # self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def laborReleaseFormRejected(self):
        self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
        self.releaseReason = self.formHistory.releaseForm.reasonForRelease
        self.template("Labor Release Form Rejected For Student",
                      "Labor Release Form Rejected For Supervisor")
        # releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Rejected For Student")
        # self.sendEmail(releaseEmailTemplateID, "student")
        #
        # SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Release Form Rejected For Supervisor")
        # self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def LaborOverLoadFormSubmitted(self, link):
        """
        For the student email, the process will work as such:
        First, the student UI HTML shell will be populated with the neccesary data.
        Once populated, the HTML shell will be converted into a link. This link
        will then be used to replace the keyword "@@link@@" in the email template.
        Once this is finished, the email can then be sent.
        """
        self.link = link
        self.template("Labor Overload Form Submitted For Student",
                      "Labor Overload Form Submitted For Supervisor")
        # releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Submitted For Student")
        # self.sendEmail(releaseEmailTemplateID, "student")
        #
        # SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Submitted For Supervisor")
        # self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def LaborOverLoadFormApproved(self):
        self.template("Labor Overload Form Approved For Student",
                      "Labor Overload Form Approved For Supervisor")
        # releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Approved For Student")
        # self.sendEmail(releaseEmailTemplateID, "student")
        #
        # SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Approved For Supervisor")
        # self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    def LaborOverLoadFormRejected(self):
        self.template("Labor Overload Form Rejected For Student",
                      "Labor Overload Form Rejected For Supervisor")
        # releaseEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Rejected For Student")
        # self.sendEmail(releaseEmailTemplateID, "student")
        #
        # SupervisorEmailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Overload Form Rejected For Supervisor")
        # self.sendEmail(SupervisorEmailTemplateID, 'supervisor')

    # Depending on what the paramater 'sendTo' is set equal to, this method will send the email either to the Primary, Seconday, or the Student
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

    # This method is responsible for replacing the keyword form the templates in the database with the data in the laborStatusForm
    def replaceText(self, form):
        form = form.replace("@@Creator@@", self.formHistory.createdBy.FIRST_NAME + " " + self.formHistory.createdBy.LAST_NAME)
        # 'Supervisor' is the supervisor on the current laborStatusForm that correspond to the formID we passed in when creating the class
        form = form.replace("@@Supervisor@@", self.laborStatusForm.supervisor.FIRST_NAME + " " + self.laborStatusForm.supervisor.LAST_NAME)
        # 'Primary Supervisor' is the primary supervisor of the student who's laborStatusForm is passed in the initializer
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
        form = form.replace("@@link@@", self.link)
        return(form)

    # Depending on the department specified, this method will send an email to either SASS or Financial Aid office
    # to notify them about the overload applocation they need to approve
    def overloadVerification(self, dept, link):
        """
        For the departments email, the process will work as such:
        First, the departments UI HTML shell will be populated with the neccesary data.
        Once populated, the HTML shell will be converted into a link. This link
        will then be used to replace the keyword "@@link@@" in the email template.
        Once this is finished, the email can then be sent.
        """
        self.link = link
        if dept == "SASS":
            email = "" #In the future, this(SASS email address) should be puled from the yaml file instead of being a string
        elif dept == "Financial Aid":
            email = "" #This(financial Aid email) address should also be pull from the yaml file
        message = Message("Overload Verification",
            recipients=[email])
        emailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "SASS and Financial Aid Office")
        message.html = self.replaceText(emailTemplateID.body)
        self.mail.send(message)
