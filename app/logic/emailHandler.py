from flask import Flask, request, render_template
from flask_mail import Mail, Message
from app.config.loadConfig import*
from app.models.emailTemplate import*
from app.models.laborReleaseForm import*
from app.models.laborStatusForm import*
from app.models.overloadForm import*
from app.models.formHistory import*
from datetime import datetime
from app.models.emailTracker import *
import string
from app import app
import os
from datetime import datetime, date

class emailHandler():
    def __init__(self, formHistoryKey, primaryFormHistory=None):
        secret_conf = get_secret_cfg()

        app.config.update(
            MAIL_SERVER=secret_conf['MAIL_SERVER'],
            MAIL_PORT=secret_conf['MAIL_PORT'],
            MAIL_USERNAME= secret_conf['MAIL_USERNAME'],
            MAIL_PASSWORD= secret_conf['MAIL_PASSWORD'],
            MAIL_USE_TLS=secret_conf['MAIL_USE_TLS'],
            MAIL_USE_SSL=secret_conf['MAIL_USE_SSL'],
            MAIL_DEFAULT_SENDER=secret_conf['MAIL_DEFAULT_SENDER'],
            ALWAYS_SEND_MAIL=secret_conf['ALWAYS_SEND_MAIL']
        )

        self.primaryFormHistory = primaryFormHistory
        self.mail = Mail(app)

        self.formHistory = FormHistory.get(FormHistory.formHistoryID == formHistoryKey)
        self.laborStatusForm = self.formHistory.formID
        self.studentEmail = self.laborStatusForm.studentSupervisee.STU_EMAIL
        self.creatorEmail = self.formHistory.createdBy.EMAIL
        self.supervisorEmail = self.laborStatusForm.supervisor.EMAIL
        self.date = self.laborStatusForm.startDate.strftime("%m/%d/%Y")
        self.weeklyHours = str(self.laborStatusForm.weeklyHours)
        self.contractHours = str(self.laborStatusForm.contractHours)

        # This will either bring back the same Labor Status Form, or bring back
        # the Primary LSF that goes with any Secondary LSF in the given term
        self.primaryForm = LaborStatusForm.get(LaborStatusForm.jobType == "Primary" and LaborStatusForm.studentSupervisee == self.laborStatusForm.studentSupervisee and LaborStatusForm.termCode == self.laborStatusForm.termCode)
        self.primaryEmail = self.primaryForm.supervisor.EMAIL
        self.link = ""
        self.releaseReason = ""
        self.releaseDate = ""

        # self.primaryLaborStatusForm = None
        if self.primaryFormHistory is not None:
            self.primaryFormHistory = FormHistory.get(FormHistory.formHistoryID == primaryFormHistory)
            self.primaryLaborStatusForm = self.primaryFormHistory.formID
            self.primarySupervisorEmail = self.primaryLaborStatusForm.supervisor.EMAIL

        try:
            self.releaseDate = self.formHistory.releaseForm.releaseDate.strftime("%m/%d/%Y")
            self.releaseReason = self.formHistory.releaseForm.reasonForRelease

        except Exception as e:
            # The error you should get when the form is not a release form
            # is the 'AttributeError' error. We expect to get the 'AttributeError',
            # but if we get anything else then we want to print the error
            if e.__class__.__name__ != "AttributeError":
                print (e)

    # The methods of this class each handle a different email situation. Some of the methods need to handle
    # "primary" and "secondary" forms differently, but a majority do not need to differentiate between the two.
    # Every method will use the replaceText and sendEmail methods to acomplish the email sending.
    # The email templates are stored inside of the emailHandler model, and depending on which email template
    # is pulled from the model, and replaceText method will replace the neccesary keywords with the correct data.
    # The sendEmail method will handle all of the email sending once the email template has been populated.
    def laborStatusFormSubmitted(self):
        ## FIXME ##
        # Add a conditional to check if jobType is Prim or Sec
        if self.laborStatusForm.jobType == 'Secondary':
            self.checkRecipient("Labor Status Form Submitted For Student",
                                False,
                                "Secondary Position Labor Status Form Submitted")
        else:
            self.checkRecipient("Labor Status Form Submitted For Student",
                          "Primary Position Labor Status Form Submitted")

    def laborStatusFormApproved(self):
        if self.laborStatusForm.jobType == 'Secondary':
            self.checkRecipient("Labor Status Form Approved For Student",
                                False,
                                "Secondary Position Labor Status Form Approved")
        else:
            self.checkRecipient("Labor Status Form Approved For Student",
                          "Primary Position Labor Status Form Approved")

    def laborStatusFormRejected(self):
        if self.laborStatusForm.jobType  == 'Secondary':
            self.checkRecipient("Labor Status Form Rejected For Student",
                                False,
                                "Secondary Position Labor Status Form Rejected")
        else:
            self.checkRecipient("Labor Status Form Rejected For Student",
                          "Primary Position Labor Status Form Rejected")

    def laborStatusFormModified(self):
        self.checkRecipient("Labor Status Form Modified For Student",
                      "Labor Status Form Modified For Supervisor")

    def laborReleaseFormSubmitted(self):
        self.checkRecipient("Labor Release Form Submitted For Student",
                      "Labor Release Form Submitted For Supervisor")

    def laborReleaseFormApproved(self):
        self.checkRecipient("Labor Release Form Approved For Student",
                      "Labor Release Form Approved For Supervisor")

    def laborReleaseFormRejected(self):
        self.checkRecipient("Labor Release Form Rejected For Student",
                      "Labor Release Form Rejected For Supervisor")

    def LaborOverLoadFormSubmitted(self, link):
        """
        For the student email, the process will work as such:
        First, the student UI HTML shell will be populated with the neccesary data.
        Once populated, the HTML shell will be converted into a link. This link
        will then be used to replace the keyword "@@link@@" in the email template.
        Once this is finished, the email can then be sent.
        """
        self.link = link
        self.checkRecipient("Labor Overload Form Submitted For Student",
                      "Labor Overload Form Submitted For Supervisor")
    def LaborOverLoadFormSubmittedNotification(self):
        """
        Emails that will be sent after the student has submitted their
        reason for the overload form; One email will be just a confirmation
        email to the student and the other one will be for the labor office.
        """
        ## FIXME ##
        # Does not exist, will need to create the template
        self.checkRecipient("Labor Overload Form Submitted Notification",
                            "Labor Overload Form Submitted Notification For Labor Office")

    def LaborOverLoadFormApproved(self):
        self.checkRecipient("Labor Overload Form Approved For Student",
                      "Labor Overload Form Approved For Supervisor")

    def LaborOverLoadFormRejected(self):
        self.checkRecipient("Labor Overload Form Rejected For Student")

    def laborStatusFormSubmittedForBreak(self):
        # This is a normal form submission on break
        self.checkRecipient("Break Labor Status Form Submitted For Student",
                            "Break Labor Status Form Submitted For Supervisor")

    def notifySecondLaborStatusFormSubmittedForBreak(self):
        # This is the submission
        self.checkRecipient("Break Labor Status Form Submitted For Student",
                            "Break Labor Status Form Submitted For Supervisor on Second LSF",
                            "Break Labor Status Form Submitted For Second Supervisor")

    # def notifyPrimSupervisorSecondLaborStatusFormSubmittedForBreak(self):
    #     self.checkRecipient(False, "Break Labor Status Form Submitted For Second Supervisor")

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
        # In order to keep track of when emails to 'SAAS' and 'Financial Aid'
        # are sent, the EmailTracker will create a new entry that points back to
        # the LSF form the email is being created for.
        self.link = link
        if dept == "SAAS":
            email = "" #In the future, this(SASS email address) should be puled from the yaml file instead of being a string
        elif dept == "Financial Aid":
            email = "" #This(financial Aid email) address should also be pull from the yaml file
        message = Message("Labor Overload Form Verification",
            recipients=[email])
        emailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "SAAS and Financial Aid Office")
        newEmailTracker = EmailTracker.create(
                        formID = self.laborStatusForm.laborStatusFormID,
                        date = datetime.today().strftime('%Y-%m-%d'),
                        recipient = dept,
                        subject = emailTemplateID.subject
                        )
        message.html = self.replaceText(emailTemplateID.body)
        self.mail.send(message)

    def verifiedOverloadNotification(self):
        """ This email will be sent to Labor Admin when SAAS or Financial Aid Make
        a decision on an overload form"""
        ## FIXME ##
        # Does not exist, will need to create
        message = Message("Verified Labor Overload Form Notification",
                    recipients=[""]) # TODO: Labor Admin email
        emailTemplateID = EmailTemplate.get(EmailTemplate.purpose == "Labor Admin Notification")
        newEmailTracker = EmailTracker.create(
                        formID = self.laborStatusForm.laborStatusFormID,
                        date = datetime.today().strftime('%Y-%m-%d'),
                        recipient = 'Labor Office',
                        subject = emailTemplateID.subject
                        )
        message.html = self.replaceText(emailTemplateID.body)
        self.mail.send(message)

    def checkRecipient(self, studentEmailPurpose=False, emailPurpose=False, secondaryEmailPurpose=False):
        """
        This method will take in two to three inputs of email purposes. An email to the student is always sent.
        The method then checks whether to send the email to only the primary or both the primary and secondary supervisors.
        The method sendEmail is then called to handle the actual sending of the emails.
        """
        if studentEmailPurpose != False:
            studentEmail = EmailTemplate.get(EmailTemplate.purpose == studentEmailPurpose)
            self.sendEmail(studentEmail, "student")
        if self.laborStatusForm.jobType == 'Secondary':
            if secondaryEmailPurpose != False:
                secondaryEmail = EmailTemplate.get(EmailTemplate.purpose == secondaryEmailPurpose)
                self.sendEmail(secondaryEmail, "secondary")
            else:
                primaryEmail = EmailTemplate.get(EmailTemplate.purpose == emailPurpose)
                self.sendEmail(primaryEmail, "supervisor")
        else:
            primaryEmail = EmailTemplate.get(EmailTemplate.purpose == emailPurpose)
            if primaryEmail.audience == "Labor Office":
                self.sendEmail(primaryEmail, "Labor Office")
            else:
                print('<<<<<<<Hit the primary email button>>>>>>>')
                self.sendEmail(primaryEmail, "supervisor")
        if self.primaryFormHistory is not None:
            primaryEmail = EmailTemplate.get(EmailTemplate.purpose == emailPurpose)
            secondaryEmail = EmailTemplate.get(EmailTemplate.purpose == secondaryEmailPurpose)
            self.sendEmail(secondaryEmail, "breakPrimary")
            self.sendEmail(primaryEmail, "supervisor")


    # Depending on the parameter 'sendTo', this method will send the email either to the Primary, Secondary, or the Student
    def sendEmail(self, template, sendTo):
        formTemplate = template.body
        formTemplate = self.replaceText(formTemplate)
        if sendTo == "student":
            message = Message(template.subject,
                recipients=[self.studentEmail])
            recipient = 'Student'
        elif sendTo == "secondary":
            message = Message(template.subject,
                recipients=[self.supervisorEmail, self.primaryEmail])
            recipient = 'Secondary Supervisor'
        elif sendTo == "Labor Office":
            message = Message(template.subject,
                recipients=[""]) #TODO: Email for the Labor Office
            recipient = 'Labor Office'
        elif sendTo == "breakPrimary":
            message = Message(template.subject,
                recipients=[self.primarySupervisorEmail])
            recipient = 'Primary Break Supervisor'
        elif sendTo == 'supervisor':
            message = Message(template.subject,
                recipients=[self.supervisorEmail])
            recipient = 'Primary Supervisor'
        message.html = formTemplate

        newEmailTracker = EmailTracker.create(
                        formID = self.laborStatusForm.laborStatusFormID,
                        date = datetime.today().strftime('%Y-%m-%d'),
                        recipient = recipient,
                        subject = template.subject
                        )

        self.mail.send(message)
        # if app.config['ENV'] == 'production' or app.config['ALWAYS_SEND_MAIL']:
        #     self.mail.send(message)
        # else:
        #     print("ENV: {}. Email not sent to {}, subject '{}'.".format(app.config['ENV'], message.recipients, message.subject))

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
        if self.primaryFormHistory != None:
            form = form.replace("@@PrimarySupervisor@@", self.primaryLaborStatusForm.supervisor.FIRST_NAME +" "+ self.primaryLaborStatusForm.supervisor.LAST_NAME)
            form = form.replace("@@SupervisorEmail@@", self.supervisorEmail)
        form = form.replace("@@Date@@", self.date)
        form = form.replace("@@ReleaseReason@@", self.releaseReason)
        form = form.replace("@@ReleaseDate@@", self.releaseDate)
        form = form.replace("@@link@@", self.link)
        return(form)
