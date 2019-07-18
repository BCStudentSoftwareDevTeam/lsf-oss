from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.student import Student
from app.controllers.errors_routes.handlers import *
from app.login_manager import require_login

@main_bp.route('/laborHistory/<id>', methods=['GET', 'POST'])
# @login_required
def laborhistory(id):
    try:
        current_user = require_login()
        if not current_user:                    # Not logged in
            return render_template('errors/403.html')


        student = Student.get(Student.ID == id)
        studentForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == student)

        #for form in studentForms:
            #print(form)
        return render_template( 'main/laborhistory.html',
    				            title=('Labor History'),
                                student = student,
                                username=current_user.username,
                                studentForms = studentForms
                              )
    except:
        render_template('errors/500.html')
