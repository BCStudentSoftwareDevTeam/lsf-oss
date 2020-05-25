from flask_login import login_required
from app.controllers.main_routes import *
from app.login_manager import require_login
from app.models.user import *
from app.models.status import *
from app.models.laborStatusForm import *
from app.models.overloadForm import *
from app.models.formHistory import *
from app.models.historyType import *
from app.models.term import *
from app.models.student import Student
from app.models.Tracy.studata import *
from app.models.Tracy.stustaff import *
from app.models.department import *
from app.models.Tracy.stuposn import STUPOSN
from flask import json, jsonify
from flask import request
from datetime import datetime, date
from flask import Flask, redirect, url_for, flash
from app import cfg
from app.logic.emailHandler import*

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
                                 laborDepartmentNotes = rspFunctional["stuLaborNotes"]
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


def createBreakHistory(rspFunctional, lsf, creatorID, status):
    """
    Creates the form history during break periods (Thanksgiving, spring, fall, summer, and Christmas break)
    rspFunctional: a dictionary containing all the data submitted in the LSF page
    lsf: stores the new instance of a labor status form
    creatorID: ID of the user who submitted the LSF
    status: status of the labor status form (e.g. Pending, etc.)
    """
    termCode = str(term)[-2:]
    if "stuTotalHours" in rspFunctional and termCode in ["11", "12", "00"]: # If not a regular term (Academic Year, Fall, or Spring)
        if (rspFunctional["stuTotalHours"] > 15) and (rspFunctional["stuJobType"] == "Secondary"):
            formOverload = FormHistory.create( formID = lsf.laborStatusFormID,
                                              historyType = historyType.historyTypeName,
                                              overloadForm = newLaborOverloadForm.overloadFormID,
                                              createdBy   = creatorID,
                                              createdDate = date.today(),
                                              status      = status.statusName)
            print("before email handler")
            email = emailHandler(formOverload.formHistoryID)
            print("----------this email handler worked")
            email.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(formOverload.formHistoryID))


def emailDuringBreak(secondLSFBreak):
    """
    Sending emails during break period
    """
    # sending emails during break period
    isOneLSF = json.loads(secondLSFBreak)
    if(isOneLSF["Status"] == False): #Student has more than one lsf. Send email to both supervisors and student
        primaryFormHistoryID = ""
        if(isOneLSF["lsfFormID"] != []): # if there is only one labor status form, do nothing. Otherwise, send emails to the previous supervisors
            for lsfID in isOneLSF["lsfFormID"]: # send email per previous lsf form
                primaryFormHistories = FormHistory.select().where(FormHistory.formID == lsfID)
                for primaryFormHistory in primaryFormHistories:
                    primaryFormHistoryID = primaryFormHistory.formHistoryID
                emailPrimSupBreakLSF = emailHandler(formHistory.formHistoryID, primaryFormHistoryID)
                emailPrimSupBreakLSF.notifyPrimSupervisorSecondLaborStatusFormSubmittedForBreak() #send email to all of the previous supervisors
            emailForBreakLSF = emailHandler(formHistory.formHistoryID, primaryFormHistoryID)
            emailForBreakLSF.notifySecondLaborStatusFormSubmittedForBreak() #send email to student and supervisor for the current lsf break form
    else: # Student has only one lsf, send email to student and supervisor
        email = emailHandler(formHistory.formHistoryID)
        email.laborStatusFormSubmittedForBreak()
