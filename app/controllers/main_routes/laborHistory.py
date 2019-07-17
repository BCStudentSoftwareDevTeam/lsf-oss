from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import LaborStatusForm
from app.models.student import Student

@main_bp.route('/laborHistory/<id>', methods=['GET', 'POST'])
# @login_required
def laborhistory(id):
    username = load_user('heggens')
    student = Student.get(Student.ID == id)
    studentForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == student)

    return render_template( 'main/laborhistory.html',
				            title=('Labor History'),
                            username = username,
                            studentForms = studentForms
                          )
