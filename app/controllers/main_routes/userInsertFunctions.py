from app.controllers.main_routes import *
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

def getOrCreateStudentData(rspFunctional):
    tracyStudent = STUDATA.get(ID = rspFunctional['stuBNumber']) #Gets student info from Tracy
    #Tries to get a student with the followin information from the database
    #if the student doesn't exist, it tries to create a student with that same information
    d, created = Student.get_or_create(ID = tracyStudent.ID,
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

def createLaborStatusForm(rspFunctional):
    tracyStudent = STUDATA.get(ID = rspFunctional['stuBNumber'])
    student = Student.get(ID = tracyStudent.ID)
    student = Student.get(ID = tracyStudent.ID)
    studentID = student.ID
    d, created = User.get_or_create(UserID = rspFunctional['stuSupervisorID'])
    primarySupervisor = d.UserID
    d, created = Department.get_or_create(DEPT_NAME = rspFunctional['stuDepartment'])
    department = d.departmentID
    d, created = Term.get_or_create(termCode = rspFunctional['stuTermCode'])
    term = d.termCode
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
                                 supervisorNotes = rspFunctional["stuNotes"]
                                 )
    return lsf

def createFormHistory(rspFunctional, lsf):
    if rspFunctional.get("isItOverloadForm") == "True":
        historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form")
    else:
        historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Status Form")
    status = Status.get(Status.statusName == "Pending")
    d, created = User.get_or_create(username = cfg['user']['debug'])
    creatorID = d.UserID
    formHistory = FormHistory.create( formID = lsf.laborStatusFormID,
                                      historyType = historyType.historyTypeName,
                                      createdBy   = creatorID,
                                      createdDate = date.today(),
                                      status      = status.statusName)

def createLaborOverloadForm(rspFunctional, lsf):
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
    historyType = HistoryType.get(HistoryType.historyTypeName == "Labor Overload Form")
    status = Status.get(Status.statusName == "Pending")
    d, created = User.get_or_create(username = cfg['user']['debug'])
    creatorID = d.UserID
    if(rspFunctional["stuTotalHours"]) != None:
        if (rspFunctional["stuTotalHours"] > 15) and (rspFunctional["stuJobType"] == "Secondary"):
            formOverload = FormHistory.create( formID = lsf.laborStatusFormID,
                                              historyType = historyType.historyTypeName,
                                              overloadForm = newLaborOverloadForm.overloadFormID,
                                              createdBy   = creatorID,
                                              createdDate = date.today(),
                                              status      = status.statusName)
            email = emailHandler(formOverload.formHistoryID)
            email.LaborOverLoadFormSubmitted('http://{0}/'.format(request.host) + 'studentOverloadApp/' + str(formOverload.formHistoryID))
