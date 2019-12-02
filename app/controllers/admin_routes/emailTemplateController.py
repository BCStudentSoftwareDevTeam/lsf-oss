from app.controllers.admin_routes import *
from app.models.user import *
from app.controllers.admin_routes import admin
from app.models.emailTemplate import *


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
