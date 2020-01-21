from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.emailTemplate import *
from flask import Flask, redirect, url_for, flash, jsonify, json, request, flash


@admin.route('/admin/emailTemplates', methods=['GET'])
# @login_required
def email_templates():
    emailTemplateID = EmailTemplate.select()
    purpose = EmailTemplate.select()
    subject = EmailTemplate.select()
    body = EmailTemplate.select()
    return render_template( 'admin/emailTemplates.html',
				            title=('Email Templates'),
                            emailTemplateID = emailTemplateID,
                            purpose = purpose,
                            subject = subject,
                            body = body
                          )

@admin.route('/admin/emailTemplates/getPurpose/<recipient>', methods=['GET'])

def getPurpose(recipient):
    try:
        emailPurposes = EmailTemplate.select(EmailTemplate.purpose).where(EmailTemplate.audience == recipient)
        purposeList = []
        for i in emailPurposes:
            purposeList.append({"Purpose":i.purpose})
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

@admin.route('/admin/emailTemplates/postEmail/', methods=['POST'])

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
