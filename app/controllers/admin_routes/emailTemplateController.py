from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.emailTemplate import *
from flask import Flask, redirect, url_for, flash, jsonify


@admin.route('/admin/emailTemplates', methods=['GET', 'POST'])
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



@admin.route('/admin/emailTemplates/<recipient>', methods=['GET', 'POST'])

def getPurpose(recipient):
    try:
        print("Made it here")
        print(recipient)
        emailPurposes = EmailTemplate.select(EmailTemplate.purpose).where(EmailTemplate.audience == recipient)
        for i in emailPurposes:
            print (i.purpose)
        return (jsonify({"Success": True}))
    except Exception as e:
        print(e)
        return jsonify({"Success": False})
