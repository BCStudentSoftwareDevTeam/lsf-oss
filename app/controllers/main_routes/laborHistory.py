from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.formHistory import *
from app.models.student import *
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
        # print(student)
        studentForms = LaborStatusForm.select().where(LaborStatusForm.studentSupervisee == student)
        # print("Here")
        # try:
        #     for k in studentForms:
        #         print(k)
        # except Exception as e:
        #     print(e)
        # forms = FormHistory.select()
        # try:
        #     for i in forms:
        #         print(i)
        # except Exception as e:
        #     print(e)
        # print("Down here")
        # print(studentForms)
        # try:
        #     for i in studentForms:
        #         print(i.formID.studentSupervisee.FIRST_NAME)
        # except Exception as e:
        #     print(e)
        # try:
        #     print(studentForms.formID.studentSupervisee.FIRST_NAME)
        # except Exception as e:
        #     print(e)

        #for form in studentForms:
            #print(form)
        return render_template( 'main/laborhistory.html',
    				            title=('Labor History'),
                                student = student,
                                username=current_user.username,
                                studentForms = studentForms,
                                #forms = forms
                              )
    except:
        render_template('errors/500.html')

@main_bp.route('/laborHistory/modal/<statusKey>', methods=['GET'])

def populateModal(statusKey):
    try:
        forms = FormHistory.select().where(FormHistory.formID == statusKey)
        modalData = {}
        for i in forms:
            print(i.formID.WLS)
            print(i.formID.studentSupervisee.FIRST_NAME)
            modalData[statusKey] = {"createdDate": i.rejectReason}
        print(statusKey)
        print(modalData)
        modalData[statusKey] = {""}
        return (jsonify({"Success": True}))
    except Exception as e:
        print(e)
        return (jsonify({"Success": False}))
