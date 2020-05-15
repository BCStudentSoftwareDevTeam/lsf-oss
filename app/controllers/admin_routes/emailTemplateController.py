from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.emailTemplate import *
from app.login_manager import require_login
from flask import Flask, redirect, url_for, flash, jsonify, json, request, flash

@admin.route('/admin/emailTemplates', methods=['GET'])
# @login_required
def email_templates():
    current_user = require_login()
    if not current_user:                    # Not logged in
        return render_template('errors/403.html')
    if not current_user.isLaborAdmin:       # Not a labor admin
        isLaborAdmin = False
        return render_template('errors/403.html',
                                isLaborAdmin = isLaborAdmin)
    else:
        isLaborAdmin = True
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
                            body = body,
                            isLaborAdmin = isLaborAdmin
                          )

@admin.route('/admin/emailTemplates/getEmailArray/', methods=['GET'])

def getEmailArray():
    print("in AJAX")
    response = EmailTemplate.select()
    # for i in response:
    #     print(i.audience)
    emailTemplateArrayDict = []
    for i in range(len(response)):
        currentTemplateDict = { "ID": response[i].emailTemplateID,
                                "purpose": response[i].purpose,
                                "subject": response[i].subject,
                                "body": str(response[i].body),
                                "audience": response[i].audience,
                                "formType": response[i].formType,
                                "action": response[i].action
                              }
        emailTemplateArrayDict.append(currentTemplateDict)
        break
    print("emailTemplate: ", emailTemplateArrayDict)
    print("---response: ", type(response))
    return json.dumps((emailTemplateArrayDict))

@admin.route('/admin/emailTemplates/getPurpose/<fieldsDictSTR>', methods=['GET'])

def getPurpose(fieldsDictSTR):
    try:
        fieldsDict = json.loads(fieldsDictSTR)
        emailPurposes = EmailTemplate.select(EmailTemplate.purpose)
        # populate the Purpose dropdown depending on other dropdowns' values
        if len(fieldsDict['recipient']) > 0:
            emailPurposes = emailPurposes.select(EmailTemplate.purpose).where(EmailTemplate.audience == fieldsDict['recipient'])
        if len(fieldsDict['formType']) > 0:
            emailPurposes = emailPurposes.select(EmailTemplate.purpose).where(EmailTemplate.formType == fieldsDict['formType'])
        if len(fieldsDict['action']) > 0:
            emailPurposes = emailPurposes.select(EmailTemplate.purpose).where(EmailTemplate.action == fieldsDict['action'])

        purposeList = []
        for i in range(len(emailPurposes)):
            purposeList.append({"Purpose":emailPurposes[i].purpose})
        return json.dumps(purposeList)
    except Exception as e:
        print(e)
        return jsonify({"Success": False})

@admin.route('/admin/emailTemplates/getEmail/<purpose>', methods=['GET'])

def getEmail(purpose):
    try:
        email = EmailTemplate.get(EmailTemplate.purpose == purpose)
        purposeList = {"emailBody": email.body, "emailSubject": email.subject}
        return json.dumps(purposeList)
    except Exception as e:
        print(e)
        return jsonify({"Success": False})

@admin.route('/admin/emailTemplates/postEmail', methods=['POST'])
def postEmail():
    try:
        email = EmailTemplate.get(EmailTemplate.purpose == request.form['purpose'])
        email.body = request.form['body']
        email.save()
        flash("The email template has been successfully updated.", "success")
        return (jsonify({"Success": True}))
    except Exception as e:
        print(e)
        return jsonify({"Success": False})
