from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.emailTemplate import *
from app.login_manager import require_login
from flask import Flask, redirect, url_for, flash, jsonify, json, request, flash

@admin.route('/admin/emailTemplates', methods=['GET'])
# @login_required
def email_templates():
    currentUser = require_login()
    if not currentUser:                    # Not logged in
        return render_template('errors/403.html'), 403
    if not currentUser.isLaborAdmin:       # Not a labor admin
        if currentUser.Student: # logged in as a student
            return redirect('/laborHistory/' + currentUser.Student.ID)
        elif currentUser.Supervisor:
            return render_template('errors/403.html'), 403
    emailTemplateID = EmailTemplate.select()
    purpose = EmailTemplate.select(EmailTemplate.purpose).distinct()
    formType = EmailTemplate.select(EmailTemplate.formType).distinct()
    action = EmailTemplate.select(EmailTemplate.action).distinct()
    subject = EmailTemplate.select(EmailTemplate.subject).distinct()
    recipient = EmailTemplate.select(EmailTemplate.audience).distinct()
    body = EmailTemplate.select(EmailTemplate.body)
    return render_template( 'admin/emailTemplates.html',
				            title=('Email Templates'),
                            emailTemplateID = emailTemplateID,
                            purpose = purpose,
                            action = action,
                            formType = formType,
                            subject = subject,
                            recipient = recipient,
                            body = body
                          )

@admin.route('/admin/emailTemplates/getEmailArray/', methods=['GET'])

def getEmailArray():
    response = EmailTemplate.select()
    emailTemplateArrayDict = []
    for i in range(len(response)):
        currentTemplateDict = { "ID": response[i].emailTemplateID,
                                "purpose": response[i].purpose,
                                "subject": response[i].subject,
                                "body": response[i].body,
                                "audience": response[i].audience,
                                "formType": response[i].formType,
                                "action": response[i].action
                              }
        emailTemplateArrayDict.append(currentTemplateDict)

    return json.dumps(emailTemplateArrayDict)

@admin.route('/admin/emailTemplates/getPurpose/<fieldsDictSTR>', methods=['GET'])

def getPurpose(fieldsDictSTR):
    try:
        fieldsDict = json.loads(fieldsDictSTR)
        # populate the Subject field depending on other dropdowns' values
        emailSubjects = EmailTemplate.select(EmailTemplate.subject).where(EmailTemplate.audience == fieldsDict['recipient'], EmailTemplate.formType == fieldsDict['formType'], EmailTemplate.action == fieldsDict['action'])
        subjectList = []
        subjectList.append({"Subject":emailSubjects[0].subject})
        return json.dumps(subjectList)
    except Exception as e:
        print("ERROR in getPurpose(): ", e)
        return jsonify({"Success": False}), 500

@admin.route('/admin/emailTemplates/getEmail/<fieldsDictSTR>', methods=['GET'])

def getEmail(fieldsDictSTR):
    try:
        fieldsDict = json.loads(fieldsDictSTR)
        email = EmailTemplate.get(EmailTemplate.action == fieldsDict["action"], EmailTemplate.audience == fieldsDict["recipient"], EmailTemplate.formType == fieldsDict["formType"])
        purposeList = {"emailBody": email.body, "emailSubject": email.subject}
        return json.dumps(purposeList)
    except Exception as e:
        print("ERROR getEmail(): ", e)
        return jsonify({"Success": False})

@admin.route('/admin/emailTemplates/postEmail', methods=['POST'])
def postEmail():
    try:
        email = EmailTemplate.get(EmailTemplate.audience == request.form['recipient'], EmailTemplate.formType == request.form['formType'], EmailTemplate.action == request.form['action'])
        email.body = request.form['body']
        email.subject = request.form["purpose"]
        email.save()
        message = "The Email Template '{0} {1} {2}' has been successfully updated.".format(email.audience, email.formType, email.action)
        flash(message, "success")
        return (jsonify({"Success": True}))
    except Exception as e:
        print("ERROR in postEmail: ", e)
        return jsonify({"Success": False})
