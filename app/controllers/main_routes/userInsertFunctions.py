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

###########################################
#1. getOrCreateStudentData()
def getOrCreateStudentData(tracyStudent):
    """
    Get a student with the followin information from the database
    if the student doesn't exist, it tries to create a student with that same information
    """
    # print("---- Tracy student: " + str(tracyStudent))

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


#2. createLaborStatusForm()
def createLaborStatusForm(tracyStudent, studentID, primarySupervisor, department, term, rspFunctional):
    """

    """
    print("----- We are in createLSF")
    # Changes the dates into the appropriate format for the table
    startDate = datetime.strptime(rspFunctional['stuStartDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
    endDate = datetime.strptime(rspFunctional['stuEndDate'], "%m/%d/%Y").strftime('%Y-%m-%d')
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

# #3. createOvrloadFormAndFormHistory()
def createOverloadFormAndFormHistory(rspFunctional, lsf, creatorID, status):
    """

    """
    if rspFunctional["isItOverloadForm"] == "True":
        historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form")
        newLaborOverloadForm = OverloadForm.create( overloadReason = "None",
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
    else:
        historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Status Form")
        FormHistory.create( formID = lsf.laborStatusFormID,
                                            historyType = historyType.historyTypeName,
                                            overloadForm = None,
                                            createdBy   = creatorID,
                                            createdDate = date.today(),
                                            status      = status.statusName)

# #4. createBreakHistory
def createBreakHistory(rspFunctional, lsf, creatorID, status):
    """

    """
    termCode = str(term)[-2:]
    if "stuTotalHours" in rspFunctional and termCode in ["11", "12", "00"]:
        if (rspFunctional["stuTotalHours"] > 15) and (rspFunctional["stuJobType"] == "Secondary"):
            formOverload = FormHistory.create( formID = lsf.laborStatusFormID,
                                              historyType = historyType.historyTypeName,
                                              overloadForm = newLaborOverloadForm.overloadFormID,
                                              createdBy   = creatorID,
                                              createdDate = date.today(),
                                              status      = status.statusName)
            email = emailHandler(formOverload.formHistoryID)
            email.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(formOverload.formHistoryID))


# #5. emailHandler()
def emailHandler(secondLSFBreak):
    """
    Sending emails during break period
    """
    # sending emails during break period
    isOneLSF = json.loads(secondLSFBreak)
    if(isOneLSF["Status"] == False): #Student has more than one lsf. Send email to both supervisors and student
        print("Before the list")
        primaryFormHistoryID = ""
        if(isOneLSF["lsfFormID"] != []): # if there is only one labor status form, do nothing. Otherwise, send emails to the previous supervisors
            print("False")
            for lsfID in isOneLSF["lsfFormID"]: # send email per previous lsf form
                primaryFormHistories = FormHistory.select().where(FormHistory.formID == lsfID)
                for primaryFormHistory in primaryFormHistories:
                    primaryFormHistoryID = primaryFormHistory.formHistoryID
                emailPrimSupBreakLSF = emailHandler(formHistory.formHistoryID, primaryFormHistoryID)
                emailPrimSupBreakLSF.notifyPrimSupervisorSecondLaborStatusFormSubmittedForBreak() #send email to all of the previous supervisors
            emailForBreakLSF = emailHandler(formHistory.formHistoryID, primaryFormHistoryID)
            emailForBreakLSF.notifySecondLaborStatusFormSubmittedForBreak() #send email to student and supervisor for the current lsf break form
    else: # Student has only one lsf, send email to student and supervisor
        print("True")
        email = emailHandler(formHistory.formHistoryID)
        email.laborStatusFormSubmittedForBreak()
