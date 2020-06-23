from flask_login import login_required
from app.controllers.main_routes import *
from app.models.user import *
from app.models.status import *
from app.models.laborStatusForm import *
from app.models.overloadForm import *
from app.models.formHistory import*
from app.models.historyType import *
from app.models.term import *
from app.models.student import Student
from app.models.Tracy.stustaff import *
from app.models.department import *
from flask import json, jsonify
from flask import request
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash
from app import cfg
from app.logic.emailHandler import emailHandler
from app.logic.tracy import Tracy, InvalidQueryException

class InvalidUserException(Exception):
    pass

def createUserFromTracy(username):
    """
        Attempts to add a user from the Tracy database to the application, based on the provided username.
        XXX Currently only handles adding staff. XXX

        Raises InvalidUserException if this does not succeed.
    """

    email = "{}@berea.edu".format(username)
    try:
        tracyUser = STUSTAFF.get(EMAIL=email)
    except DoesNotExist as e:
        raise InvalidUserException("{} not found in Tracy database".format(email))

    data = {
        'PIDM': tracyUser.PIDM,
        'username': username,
        'FIRST_NAME': tracyUser.FIRST_NAME,
        'LAST_NAME': tracyUser.LAST_NAME,
        'ID': tracyUser.ID,
        'EMAIL': email,
        'CPO': tracyUser.CPO,
        'ORG': tracyUser.ORG,
        'DEPT_NAME': tracyUser.DEPT_NAME,
        'isLaborAdmin': False,
        'isFinancialAidAdmin': False,
        'isSaasAdmin': False,
    }

    try:
        user = User.create(**data)
        return user
    except Exception as e:
        raise InvalidUserException("Adding {} to user table failed".format(username), e)

def getOrCreateStudentData(tracyStudent):
    """
    Get a student with the followin information from the database
    if the student doesn't exist, it tries to create a student with that same information
    tracyStudent: object with all the student's information from Tracy
    """
    d, created = Student.get_or_create( ID = tracyStudent.ID,
                                        FIRST_NAME = tracyStudent.FIRST_NAME,
                                        LAST_NAME = tracyStudent.LAST_NAME,
                                        CLASS_LEVEL = tracyStudent.CLASS_LEVEL,
                                        ACADEMIC_FOCUS = tracyStudent.ACADEMIC_FOCUS,
                                        MAJOR = tracyStudent.MAJOR,
                                        PROBATION = tracyStudent.PROBATION,
                                        ADVISOR = tracyStudent.ADVISOR,
                                        STU_EMAIL = tracyStudent.STU_EMAIL,
                                        STU_CPO = tracyStudent.STU_CPO,
                                        LAST_POSN = tracyStudent.LAST_POSN,
                                        LAST_SUP_PIDM = tracyStudent.LAST_SUP_PIDM)


def createLaborStatusForm(tracyStudent, studentID, primarySupervisor, department, term, rspFunctional):
    """
    Creates a labor status form with the appropriate data passed from userInsert() in laborStatusForm.py
    tracyStudent: object with all the student's information from Tracy
    studentID: student's primary ID in the database AKA their B#
    primarySupervisor: primary supervisor of the student
    department: department the position is a part of
    term: term when the position will happen
    rspFunctional: a dictionary containing all the data submitted in the LSF page
    returns the laborStatusForm object just created for later use in laborStatusForm.py
    """
    # Changes the dates into the appropriate format for the table
    startDate = datetime.strptime(rspFunctional['stuStartDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
    endDate = datetime.strptime(rspFunctional['stuEndDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
    # Creates the labor Status form
    lsf = LaborStatusForm.create(termCode_id = term,
                                 studentSupervisee_id = studentID,
                                 supervisor_id = primarySupervisor,
                                 department_id  = department,
                                 jobType = rspFunctional["stuJobType"],
                                 WLS = rspFunctional["stuWLS"],
                                 POSN_TITLE = rspFunctional["stuPosition"],
                                 POSN_CODE = rspFunctional["stuPositionCode"],
                                 contractHours = rspFunctional.get("stuContractHours", None),
                                 weeklyHours   = rspFunctional.get("stuWeeklyHours", None),
                                 startDate = startDate,
                                 endDate = endDate,
                                 supervisorNotes = rspFunctional["stuNotes"],
                                 laborDepartmentNotes = rspFunctional["stuLaborNotes"],
                                 studentName = rspFunctional["stuName"]
                                 )

    return lsf


def createOverloadFormAndFormHistory(rspFunctional, lsf, creatorID, status):
    """
    Creates an overload form and a form history if the request needs an overload, otherwise, creates only a form history
    rspFunctional: a dictionary containing all the data submitted in the LSF page
    lsf: stores the new instance of a labor status form
    creatorID: id of the user submitting the labor status form
    status: status of the labor status form (e.g. Pending, etc.)
    """
    # If the LSF is an overload form, create its history as such and an overload form
    if rspFunctional.get("isItOverloadForm") == "True":
        historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form")
        newLaborOverloadForm = OverloadForm.create( studentOverloadReason = None,
                                                    financialAidApproved = None,
                                                    financialAidApprover = None,
                                                    financialAidReviewDate = None,
                                                    SAASApproved = None,
                                                    SAASApprover = None,
                                                    SAASReviewDate = None,
                                                    laborApproved = None,
                                                    laborApprover = None,
                                                    laborReviewDate = None)
        formOverload = FormHistory.create( formID = lsf.laborStatusFormID,
                                            historyType = historyType.historyTypeName,
                                            overloadForm = newLaborOverloadForm.overloadFormID,
                                            createdBy   = creatorID,
                                            createdDate = date.today(),
                                            status      = status.statusName)
        # email = emailHandler(formOverload.formHistoryID)
        # email.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(formOverload.formHistoryID))
    else: # If not overload, create its history as a regular LSF
        historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Status Form")
        FormHistory.create( formID = lsf.laborStatusFormID,
                            historyType = historyType.historyTypeName,
                            overloadForm = None,
                            createdBy   = creatorID,
                            createdDate = date.today(),
                            status      = status.statusName)

def emailDuringBreak(secondLSFBreak, term):
    """
    Sending emails during break period
    """
    termCode = str(term)[-2:]
    if termCode not in ["11", "12", "00"]: # If not a regular term (Academic Year, Fall, or Spring)
        isOneLSF = json.loads(secondLSFBreak)
        formHistory = FormHistory.get(FormHistory.formHistoryID == isOneLSF['formHistoryID'])
        if(isOneLSF["Status"] == False): #Student has more than one lsf. Send email to both supervisors and student
            for lsfID in isOneLSF["lsfFormID"]: # send email per previous lsf form
                email = emailHandler(formHistory.formHistoryID, lsfID)
                email.notifySecondLaborStatusFormSubmittedForBreak()
        else: # Student has only one lsf, send email to student and supervisor
            email = emailHandler(formHistory.formHistoryID)
            email.laborStatusFormSubmittedForBreak()
