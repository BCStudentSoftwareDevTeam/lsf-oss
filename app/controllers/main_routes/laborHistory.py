from flask import render_template , flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.laborStatusForm import *
from app.models.formHistory import *
from app.models.student import *
from app.controllers.errors_routes.handlers import *
from app.login_manager import require_login
from flask import json
from flask import make_response
import datetime
from datetime import date

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
        return render_template( 'main/laborhistory.html',
    				            title=('Labor History'),
                                student = student,
                                username=current_user.username,
                                studentForms = studentForms,
                              )
    except:
        render_template('errors/500.html')

@main_bp.route('/laborHistory/modal/<statusKey>', methods=['GET'])

def populateModal(statusKey):
    # try:
    #     forms = FormHistory.select().where(FormHistory.formID == statusKey)
    #     print(statusKey)
    #     for k in forms:
    #         print(k.modifiedForm)
    #     modalData = {}
    #     for i in forms:
    #         modalData.update({"createdDate": i.createdDate,
    #                         "createdBy": i.createdBy.FIRST_NAME + " " + i.createdBy.LAST_NAME,
    #                         "jobType": i.formID.jobType,
    #                         "WLS": i.formID.WLS,
    #                         "contractHours": i.formID.contractHours,
    #                         "weeklyHours": i.formID.weeklyHours,
    #                         "supervisorNotes": i.formID.supervisorNotes,
    #                         "term": i.formID.termCode.termName,
    #                         "positionTitle": i.formID.POSN_TITLE,
    #                         "positionCode": i.formID.POSN_CODE,
    #                         "studentName": i.formID.studentSupervisee.FIRST_NAME + " " + i.formID.studentSupervisee.LAST_NAME
    #                         })
    #     return json.dumps(modalData)
    # except Exception as e:
    #     print(e)
    #     return (jsonify({"Success": False}))
    try:
        forms = FormHistory.select().where(FormHistory.formID == statusKey).order_by(FormHistory.createdDate.desc())
        statusForm = LaborStatusForm.select().where(LaborStatusForm.laborStatusFormID == statusKey)
        currentDate = datetime.date.today()
        # print(currentDate)
        # print("here")
        # print(statusKey)
        buttonState = None
        # for i in forms:
        #     #if i.status.statusName == "Approved":
        #     print(i.historyType.historyTypeName)
        for form in forms:
            print("Start here")
            if form.releaseForm != None:
                if form.status.statusName == "Approved":
                    print("Enter here")
                    print("End here")
                    buttonState = 0 #Only rehire button
                    break
            print("Then here")
            if form.overloadForm != None:
                if form.status.statusName == "Pending":
                    buttonState = 1 #Only withdraw button
                    break
            print("Now here")
            if form.historyType.historyTypeName == "Labor Status Form":
                print("Made it here")
                if form.status.statusName == "Pending":
                    print("I'm pending")
                    buttonState = 2 #Withdraw and modify buttons
                    break
                elif form.status.statusName == "Denied":
                    print("I'm denied")
                    buttonState = 0 #Rehire button
                    break
                elif form.status.statusName == "Approved":
                    print("I'm approved")
                    if form.reviewedDate != None:
                        print(form.reviewedDate)
                        print(form.formID.termCode.termEnd)
                        print(currentDate)
                        buttonState = 3 #Release, modify, and rehire buttons
                        break
                    elif form.reviewedDate == None:
                        print(form.reviewedDate)
                        print(form.formID.termCode.termEnd)
                        print(currentDate)
                        buttonState = 2 #Only withdraw and modify
                        break
        print(buttonState)
        # Will use later:
        #if form.formID.termCode.termEnd >= currentDate:
        #elif form.formID.termCode.termEnd < currentDate:
        resp = make_response(render_template('snips/studentHistoryModal.html',
                                            forms = forms,
                                            statusForm = statusForm,
                                            currentDate = currentDate,
                                            buttonState = buttonState
                                            ))
        return (resp)
    except Exception as e:
        print(e)
        render_template('errors/500.html')
        return (jsonify({"Success": False}))
